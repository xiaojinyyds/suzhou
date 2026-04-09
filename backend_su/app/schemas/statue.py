"""
石像景点相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StatueBase(BaseModel):
    """石像基础 Schema"""
    name: str = Field(..., max_length=100)
    icon: Optional[str] = None
    latitude: float
    longitude: float
    radius: int = 100
    introduction: Optional[str] = None
    history: Optional[str] = None
    cultural_value: Optional[str] = None


class StatueCreate(StatueBase):
    """石像创建 Schema"""
    images: Optional[List[str]] = []
    order_index: int = 0


class StatueUpdate(BaseModel):
    """石像更新 Schema"""
    name: Optional[str] = None
    icon: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[int] = None
    introduction: Optional[str] = None
    history: Optional[str] = None
    cultural_value: Optional[str] = None
    images: Optional[List[str]] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None


class StatueResponse(StatueBase):
    """石像响应 Schema"""
    id: int
    images: List[str] = []
    order_index: int
    is_active: bool
    is_checked: bool = False  # 前端需要的字段，通过业务逻辑计算
    distance: Optional[float] = None  # 距离（米）
    created_at: datetime
    
    class Config:
        from_attributes = True
