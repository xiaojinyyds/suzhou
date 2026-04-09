"""
拍照记录相关的 Pydantic 模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PhotoBase(BaseModel):
    """拍照基础模型"""
    decoration_type: Optional[str] = None


class PhotoCreate(PhotoBase):
    """创建拍照请求"""
    pass


class PhotoResponse(PhotoBase):
    """拍照响应"""
    id: int
    user_id: int
    
    # 图片相关
    image_url: str
    oss_key: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    # 元数据
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    
    # 状态与统计
    is_public: bool = False
    is_deleted: bool = False
    view_count: int = 0
    
    # 时间戳
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic V2
