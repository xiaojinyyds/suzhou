"""
打卡记录相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CheckInCreate(BaseModel):
    """打卡创建 Schema"""
    statue_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class CheckInResponse(BaseModel):
    """打卡响应 Schema"""
    id: int
    user_id: int
    statue_id: int
    latitude: float
    longitude: float
    distance: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CheckInResult(BaseModel):
    """打卡结果 Schema"""
    success: bool
    message: str
    distance: float
    checkin: Optional[CheckInResponse] = None
