"""
订单相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    """订单项创建 Schema"""
    dessert_id: int
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """订单项响应 Schema"""
    id: int
    dessert_id: int
    dessert_name: str
    dessert_image: Optional[str] = None
    price: float
    quantity: int
    subtotal: float
    
    class Config:
        from_attributes = True


class ShippingAddress(BaseModel):
    """配送地址 Schema"""
    name: str
    phone: str
    address: str
    detail: Optional[str] = None


class OrderCreate(BaseModel):
    """订单创建 Schema"""
    items: List[OrderItemCreate]
    shipping_address: ShippingAddress
    remark: Optional[str] = None


class OrderResponse(BaseModel):
    """订单响应 Schema"""
    id: int
    order_no: str
    user_id: int
    total_amount: float
    discount_amount: float
    shipping_fee: float
    final_amount: float
    status: OrderStatus
    items: List[OrderItemResponse] = []
    created_at: datetime
    paid_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
