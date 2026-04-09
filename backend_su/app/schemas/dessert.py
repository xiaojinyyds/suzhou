"""
甜品相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DessertBase(BaseModel):
    """甜品基础 Schema"""
    name: str = Field(..., max_length=100)
    icon: Optional[str] = None
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    calories: Optional[int] = None


class DessertCreate(DessertBase):
    """甜品创建 Schema"""
    ingredients: Optional[List[str]] = []
    image_url: Optional[str] = None
    stock: int = 0
    order_index: int = 0


class DessertUpdate(BaseModel):
    """甜品更新 Schema"""
    name: Optional[str] = None
    icon: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    calories: Optional[int] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class DessertResponse(DessertBase):
    """甜品响应 Schema"""
    id: int
    ingredients: List[str] = []
    image_url: Optional[str] = None
    stock: int
    sales_count: int
    order_index: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
