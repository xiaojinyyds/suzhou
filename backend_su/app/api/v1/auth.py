"""
用户认证相关 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.core.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user_id,
)
from app.core.redis_client import redis_client
from app.core.email import email_service
from app.core.config import settings
from app.models.user import User
from app.schemas.user import (
    SendCodeRequest,
    UserRegisterRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserResponse,
)
from app.schemas.common import Response
from app.utils.helpers import generate_verification_code


router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/send-code", summary="发送验证码")
async def send_verification_code(request: SendCodeRequest):
    """发送注册/登录验证码到邮箱"""
    code = generate_verification_code(settings.VERIFICATION_CODE_LENGTH)
    cache_key = f"verification_code:{request.email}"
    if not redis_client.set(cache_key, code, expire=settings.VERIFICATION_CODE_EXPIRE):
        raise HTTPException(status_code=500, detail="验证码服务不可用")

    ok = await email_service.send_verification_code(request.email, code)
    if not ok:
        raise HTTPException(status_code=500, detail="验证码发送失败，请稍后重试")

    return {"code": 200, "message": "验证码已发送", "data": {"email": request.email, "expire_seconds": settings.VERIFICATION_CODE_EXPIRE}}


@router.post("/register", summary="用户注册")
async def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """邮箱+验证码注册。为兼容，自动生成唯一用户名。"""
    cache_key = f"verification_code:{request.email}"
    cached_code = redis_client.get(cache_key)
    if not cached_code or str(cached_code).strip() != str(request.code).strip():
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 邮箱唯一性
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    # 生成唯一用户名
    base_username = (request.nickname or request.email.split('@')[0]).strip() or "user"
    username = base_username
    suffix = 1
    while db.query(User).filter(User.username == username).first() is not None:
        suffix += 1
        username = f"{base_username}{suffix}"

    user = User(
        username=username,
        email=request.email,
        password_hash=get_password_hash(request.password),
        nickname=request.nickname or base_username,
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 删除验证码
    redis_client.delete(cache_key)

    token = create_access_token({"sub": str(user.id)})
    return {"code": 200, "message": "注册成功", "data": {"access_token": token, "token_type": "bearer", "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "theme": user.theme,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
    }}}


@router.post("/login", summary="用户登录")
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """支持用户名/邮箱/手机号登录"""
    user = db.query(User).filter(
        or_(User.username == request.account, User.email == request.account, User.phone == request.account)
    ).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    token = create_access_token({"sub": str(user.id)})
    return {"code": 200, "message": "登录成功", "data": {"access_token": token, "token_type": "bearer", "user": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "theme": user.theme,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
    }}}


@router.get("/me", summary="获取当前用户信息")
async def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "message": "获取成功", "data": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "theme": user.theme,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }}


@router.put("/update-profile", summary="更新用户信息")
async def update_profile(
    request: dict,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 允许更新字段：nickname, phone, avatar_url, email(可选，需唯一)
    if 'nickname' in request:
        user.nickname = request['nickname']

    if 'phone' in request and request['phone']:
        exists = db.query(User).filter(User.phone == request['phone'], User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="该手机号已被其他用户使用")
        user.phone = request['phone']

    if 'email' in request and request['email']:
        exists = db.query(User).filter(User.email == request['email'], User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="该邮箱已被其他用户使用")
        user.email = request['email']

    if 'avatar_url' in request:
        user.avatar_url = request['avatar_url']
        
    if 'theme' in request:
        user.theme = request['theme']

    db.commit()
    db.refresh(user)

    return {"code": 200, "message": "更新成功", "data": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "theme": user.theme,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }}


@router.post("/change-password", summary="修改当前密码")
async def change_password(
    request: dict,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    old_password = request.get('old_password', '')
    new_password = request.get('new_password', '')
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码错误")

    user.password_hash = get_password_hash(new_password)
    db.commit()

    return {"code": 200, "message": "密码修改成功"}


@router.post("/forgot-password", summary="忘记密码-发送验证码")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="该邮箱尚未注册")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    code = generate_verification_code(settings.VERIFICATION_CODE_LENGTH)
    cache_key = f"reset_password_code:{request.email}"
    if not redis_client.set(cache_key, code, expire=settings.VERIFICATION_CODE_EXPIRE):
        raise HTTPException(status_code=500, detail="验证码服务不可用")

    try:
        await email_service.send_verification_code(request.email, code, purpose="重置密码")
    except Exception:
        # 邮件失败不暴露细节
        pass

    if settings.DEBUG:
        print(f"[开发模式] 重置密码验证码: {code}")

    return {"code": 200, "message": "验证码已发送到您的邮箱", "data": {"email": request.email, "expire_seconds": settings.VERIFICATION_CODE_EXPIRE}}


@router.post("/reset-password", summary="重置密码")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    cache_key = f"reset_password_code:{request.email}"
    cached_code = redis_client.get(cache_key)
    if not cached_code or str(cached_code).strip() != str(request.code).strip():
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.password_hash = get_password_hash(request.new_password)
    db.commit()
    redis_client.delete(cache_key)

    return {"code": 200, "message": "密码重置成功，请使用新密码登录"}
