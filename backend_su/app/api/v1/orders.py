"""
订单相关 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.common import Response

router = APIRouter(prefix="/orders", tags=["订单"])


@router.post("", response_model=Response[OrderResponse], summary="创建订单")
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    创建订单
    - **items**: 订单项列表
    - **shipping_address**: 配送地址
    - **remark**: 备注（可选）
    """
    # TODO: 实现创建订单逻辑
    # 1. 验证用户
    # 2. 验证商品库存
    # 3. 计算订单金额
    # 4. 生成订单号
    # 5. 保存订单
    return Response(message="订单创建成功", data=None)


@router.get("/my", response_model=Response[List[OrderResponse]], summary="获取我的订单")
async def get_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的订单列表
    """
    # TODO: 实现获取订单列表逻辑
    return Response(message="获取成功", data=[])


@router.get("/{order_id}", response_model=Response[OrderResponse], summary="获取订单详情")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    根据 ID 获取订单详情
    """
    # TODO: 实现获取订单详情逻辑
    return Response(message="获取成功", data=None)


@router.post("/{order_id}/pay", response_model=Response, summary="支付订单")
async def pay_order(order_id: int, db: Session = Depends(get_db)):
    """
    支付订单（简化版）
    """
    # TODO: 实现支付逻辑
    return Response(message="支付成功", data=None)


@router.post("/{order_id}/cancel", response_model=Response, summary="取消订单")
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """
    取消订单
    """
    # TODO: 实现取消订单逻辑
    return Response(message="取消成功", data=None)
