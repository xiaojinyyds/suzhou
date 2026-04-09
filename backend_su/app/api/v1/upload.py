"""
文件上传相关 API
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.oss_client import oss_client
from app.schemas.common import Response
from app.core.security import get_current_user_id
from app.core.database import get_db
from app.models.user import User
import io
from PIL import Image
import uuid
from pathlib import Path

router = APIRouter(prefix="/upload", tags=["文件上传"])

# 允许的图片格式
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/photo", response_model=Response[dict], summary="上传照片")
async def upload_photo(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    上传照片到阿里云 OSS
    - 支持格式: jpg, jpeg, png, gif, webp
    - 文件大小限制: 10MB
    """
    # 验证用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 1. 验证文件类型
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。仅支持: JPG, JPEG, PNG, GIF, WEBP"
        )
    
    # 2. 读取文件内容
    contents = await file.read()
    
    # 3. 验证文件大小
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，最大支持 {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # 4. 验证是否为有效图片
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="无效的图片文件"
        )
    
    # 5. 生成唯一文件名
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    
    # 6. 上传到 OSS
    try:
        result = oss_client.upload_file(
            file_content=contents,
            filename=file.filename,
            folder="photos"
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="上传失败，请稍后重试"
            )
        
        return Response(
            message="上传成功",
            data={
                "url": result['url'],
                "size": result['size'],
                "key": result['key'],
                "filename": file.filename
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"上传失败: {str(e)}"
        )


@router.post("/avatar", response_model=Response[dict], summary="上传头像")
async def upload_avatar(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    上传用户头像
    - 支持格式: jpg, jpeg, png, webp
    - 文件大小限制: 5MB
    - 建议尺寸: 200x200 或更大
    """
    # 验证用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 1. 验证文件类型
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。仅支持: JPG, JPEG, PNG, WEBP"
        )
    
    # 2. 读取文件内容
    contents = await file.read()
    
    # 3. 验证文件大小（头像限制为5MB）
    max_avatar_size = 5 * 1024 * 1024
    if len(contents) > max_avatar_size:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，头像最大支持 5MB"
        )
    
    # 4. 验证是否为有效图片
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        
        # 重新打开图片以获取尺寸信息
        image = Image.open(io.BytesIO(contents))
        width, height = image.size
        
        # 建议尺寸检查（仅警告，不强制）
        if width < 100 or height < 100:
            print(f"警告: 头像尺寸较小 ({width}x{height})，建议至少 200x200")
    
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="无效的图片文件"
        )
    
    # 5. 生成唯一文件名
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    
    # 6. 上传到 OSS
    try:
        result = oss_client.upload_file(
            file_content=contents,
            filename=file.filename,
            folder="avatars"
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="上传失败，请稍后重试"
            )
        
        return Response(
            message="上传成功",
            data={
                "url": result['url'],
                "size": result['size'],
                "key": result['key'],
                "width": width,
                "height": height,
                "filename": file.filename
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"上传失败: {str(e)}"
        )
