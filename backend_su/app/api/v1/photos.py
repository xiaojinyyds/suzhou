"""
拍照记录相关接口
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.oss_client import oss_client
from app.models.photo import Photo
from app.schemas.common import Response
from app.schemas.photo import PhotoCreate, PhotoResponse

router = APIRouter()

# 配置本地备份目录（可选）
UPLOAD_DIR = "uploads/photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=Response[PhotoResponse], summary="上传拍照")
async def upload_photo(
    image: UploadFile = File(...),
    decoration_type: Optional[str] = Form(None),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    上传拍照图片
    - **image**: 图片文件
    - **decoration_type**: 装饰类型（可选）
    """
    try:
        # 验证文件类型
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        # 读取文件内容
        content = await image.read()
        file_size = len(content)
        
        # 上传到阿里云 OSS
        oss_result = oss_client.upload_file(
            file_content=content,
            filename=image.filename or "photo.jpg",
            folder="photos"
        )
        
        if not oss_result:
            # OSS 上传失败，回退到本地存储
            file_ext = os.path.splitext(image.filename)[1] if image.filename else '.jpg'
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            image_url = f"/uploads/photos/{unique_filename}"
            oss_key = None
            print(f"⚠️ OSS上传失败，使用本地存储: {image_url}")
        else:
            # OSS 上传成功，使用 OSS URL
            image_url = oss_result['url']
            oss_key = oss_result['key']  # 保存 OSS key 用于删除
            print(f"✅ OSS上传成功: {image_url}")
        
        # 保存到数据库
        photo = Photo(
            user_id=user_id,
            image_url=image_url,
            oss_key=oss_key,
            decoration_type=decoration_type,
            file_size=file_size,
            is_public=False  # 默认私密
        )
        
        db.add(photo)
        db.commit()
        db.refresh(photo)
        
        return Response(
            message="上传成功",
            data=photo
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@router.get("/public", response_model=Response)
async def get_public_photos(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取广场公开照片列表
    """
    query = db.query(Photo).filter(
        Photo.is_deleted == False,
        Photo.is_public == True
    )
    
    total = query.count()
    photos = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()
    
    # 手动转换为 Pydantic 模型以避免序列化错误
    items = [PhotoResponse.model_validate(p) for p in photos]
    
    return Response(
        data={
            "items": items,
            "total": total,
            "page": skip // limit + 1,
            "size": limit
        }
    )


@router.get("/my", response_model=Response, summary="获取我的拍照")
async def get_my_photos(
    skip: int = 0,
    limit: int = 20,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有拍照记录（不包括已删除）
    """
    query = db.query(Photo).filter(
        Photo.user_id == user_id,
        Photo.is_deleted == False  # 过滤掉已删除的照片
    )
    
    total = query.count()
    photos = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()
    
    # 手动转换为 Pydantic 模型
    items = [PhotoResponse.model_validate(p) for p in photos]
    
    return Response(
        message="获取成功",
        data={
            "items": items,
            "total": total,
            "page": skip // limit + 1,
            "size": limit
        }
    )


@router.delete("/{photo_id}", response_model=Response, summary="删除拍照")
async def delete_photo(
    photo_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    删除指定的拍照记录（软删除）
    """
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id,
        Photo.is_deleted == False  # 只能删除未删除的照片
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在或已被删除")
    
    # 如果有 OSS key，删除 OSS 文件
    if photo.oss_key:
        try:
            success = oss_client.delete_file(photo.oss_key)
            if success:
                print(f"✅ OSS文件删除成功: {photo.oss_key}")
            else:
                print(f"⚠️ OSS文件删除失败: {photo.oss_key}")
        except Exception as e:
            print(f"❌ OSS删除异常: {e}")
    
    # 如果是本地存储，删除本地文件
    elif photo.image_url and photo.image_url.startswith('/uploads/'):
        file_path = photo.image_url.lstrip('/')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ 本地文件删除成功: {file_path}")
            except Exception as e:
                print(f"❌ 本地文件删除失败: {e}")
    
    # 软删除：标记为已删除
    photo.is_deleted = True
    db.commit()
    
    return Response(message="删除成功")


@router.get("/stats", response_model=Response, summary="获取拍照统计")
async def get_photo_stats(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取用户的拍照统计信息
    """
    total_count = db.query(Photo).filter(
        Photo.user_id == user_id,
        Photo.is_deleted == False
    ).count()
    
    public_count = db.query(Photo).filter(
        Photo.user_id == user_id,
        Photo.is_deleted == False,
        Photo.is_public == True
    ).count()
    
    return Response(
        message="获取成功",
        data={
            "total_count": total_count,
            "public_count": public_count,
            "private_count": total_count - public_count,
            "user_id": user_id
        }
    )


@router.patch("/{photo_id}/public", response_model=Response[PhotoResponse], summary="设置照片公开状态")
async def update_photo_public_status(
    photo_id: int,
    is_public: bool = Form(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新照片的公开状态
    """
    photo = db.query(Photo).filter(
        Photo.id == photo_id,
        Photo.user_id == user_id,
        Photo.is_deleted == False
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")
    
    photo.is_public = is_public
    db.commit()
    db.refresh(photo)
    
    return Response(
        message="设置成功",
        data=photo
    )
