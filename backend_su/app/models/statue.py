"""
石像景点数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Statue(Base):
    """石像景点表"""
    __tablename__ = "statues"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="景点名称")
    icon = Column(String(50), nullable=True, comment="图标 emoji")
    latitude = Column(Float, nullable=False, comment="纬度")
    longitude = Column(Float, nullable=False, comment="经度")
    radius = Column(Integer, default=100, comment="打卡半径（米）")
    introduction = Column(Text, nullable=True, comment="简介")
    history = Column(Text, nullable=True, comment="历史背景")
    cultural_value = Column(Text, nullable=True, comment="文化价值")
    images = Column(Text, nullable=True, comment="图片URL列表（JSON）")
    order_index = Column(Integer, default=0, comment="排序序号")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
