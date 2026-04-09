"""
甜品数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Dessert(Base):
    """甜品表"""
    __tablename__ = "desserts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="甜品名称")
    icon = Column(String(50), nullable=True, comment="图标 emoji")
    price = Column(Float, nullable=False, comment="价格")
    description = Column(Text, nullable=True, comment="描述")
    ingredients = Column(Text, nullable=True, comment="配料（JSON）")
    calories = Column(Integer, nullable=True, comment="热量（卡路里）")
    image_url = Column(String(500), nullable=True, comment="图片URL")
    stock = Column(Integer, default=0, comment="库存")
    sales_count = Column(Integer, default=0, comment="销量")
    order_index = Column(Integer, default=0, comment="排序序号")
    is_active = Column(Boolean, default=True, comment="是否上架")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
