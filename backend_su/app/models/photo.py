"""
拍照记录数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Photo(Base):
    """拍照记录表"""
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    
    # 图片相关
    image_url = Column(String(500), nullable=False, comment="图片完整URL")
    oss_key = Column(String(500), nullable=True, comment="OSS存储路径(用于删除)")
    thumbnail_url = Column(String(500), nullable=True, comment="缩略图URL")
    
    # 元数据
    decoration_type = Column(String(50), default='none', comment="装饰类型")
    file_size = Column(Integer, nullable=True, comment="文件大小（字节）")
    width = Column(Integer, nullable=True, comment="图片宽度")
    height = Column(Integer, nullable=True, comment="图片高度")
    
    # 状态与统计
    is_public = Column(Boolean, default=False, nullable=False, index=True, comment="是否公开")
    is_deleted = Column(Boolean, default=False, nullable=False, index=True, comment="是否已删除")
    view_count = Column(Integer, default=0, nullable=False, comment="浏览次数")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    user = relationship("User", backref="photos")
