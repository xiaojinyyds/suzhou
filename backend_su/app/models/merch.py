from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class MerchOrder(Base):
    __tablename__ = "merch_orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    product_id = Column(String(50), nullable=False, comment="商品代号ID")
    product_name = Column(String(100), nullable=False, comment="商品名称")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="订单预约时间")
    
    user = relationship("User", backref="merch_orders")
