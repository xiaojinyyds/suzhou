"""
订单数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.user import User
from app.models.dessert import Dessert


class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"  # 待支付
    PAID = "paid"  # 已支付
    PROCESSING = "processing"  # 处理中
    SHIPPED = "shipped"  # 已发货
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    REFUNDED = "refunded"  # 已退款


class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    total_amount = Column(Float, nullable=False, comment="订单总额")
    discount_amount = Column(Float, default=0, comment="优惠金额")
    shipping_fee = Column(Float, default=0, comment="配送费")
    final_amount = Column(Float, nullable=False, comment="实付金额")
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, comment="订单状态")
    shipping_address = Column(Text, nullable=True, comment="配送地址（JSON）")
    remark = Column(Text, nullable=True, comment="备注")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    user = relationship(User, backref="orders")


class OrderItem(Base):
    """订单明细表"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True, comment="订单ID")
    dessert_id = Column(Integer, ForeignKey("desserts.id"), nullable=False, comment="甜品ID")
    dessert_name = Column(String(100), nullable=False, comment="甜品名称")
    dessert_image = Column(String(500), nullable=True, comment="甜品图片")
    price = Column(Float, nullable=False, comment="单价")
    quantity = Column(Integer, nullable=False, comment="数量")
    subtotal = Column(Float, nullable=False, comment="小计")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    order = relationship("Order", backref="items")
    dessert = relationship(Dessert)
