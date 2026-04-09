#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""安全相关：JWT、密码加密（适配 backend_su 配置）"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # 直接使用 bcrypt，避免 passlib 兼容性问题
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    # 直接使用 bcrypt，避免 passlib 兼容性问题
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌，使用 backend_su 的配置键"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """解码JWT令牌"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        print(f"JWT decode error: {e}")
        print(f"Token: {token[:50]}...")
        print(f"Secret key: {settings.JWT_SECRET_KEY[:10]}...")
        return None


security_scheme = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> int:
    """获取当前认证用户的ID（int）"""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    try:
        return int(payload["sub"])  # 将字符串的用户ID转换为整数
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(None)
):
    """获取当前用户完整信息（需要显式传入db依赖）"""
    from app.core.database import get_db
    from app.models.user import User
    
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    try:
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    # 如果没有传入db，手动创建
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        should_close = True
    else:
        should_close = False
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )
        return user
    finally:
        if should_close:
            db.close()


def verify_admin_role(user_id: int = Depends(get_current_user_id)):
    """验证当前用户是否为管理员，返回user_id"""
    from app.core.database import get_db
    from app.models.user import User
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # 验证管理员权限
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin permission required",
            )
        
        return user_id
    finally:
        db.close()


def get_admin_user(
    user_id: int = Depends(verify_admin_role),
    db: Session = Depends(None)
):
    """获取管理员用户完整信息"""
    from app.core.database import get_db
    from app.models.user import User
    
    # 如果没有传入db，手动创建
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        should_close = True
    else:
        should_close = False
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        if should_close:
            db.close()
