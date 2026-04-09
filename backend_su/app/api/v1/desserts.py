"""
甜品相关 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.dessert import DessertResponse
from app.schemas.common import Response

router = APIRouter(prefix="/desserts", tags=["甜品"])


@router.get("", response_model=Response[List[DessertResponse]], summary="获取甜品列表")
async def get_desserts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """
    获取所有甜品列表
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    # TODO: 实现获取甜品列表逻辑
    return Response(message="获取成功", data=[])


@router.get("/{dessert_id}", response_model=Response[DessertResponse], summary="获取甜品详情")
async def get_dessert(dessert_id: int, db: Session = Depends(get_db)):
    """
    根据 ID 获取甜品详情
    """
    # TODO: 实现获取甜品详情逻辑
    return Response(message="获取成功", data=None)
