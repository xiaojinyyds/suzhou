from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.merch import MerchOrder
from app.schemas.common import Response
from pydantic import BaseModel

router = APIRouter(prefix="/merch", tags=["周边预约"])

class MerchOrderCreate(BaseModel):
    product_id: str
    product_name: str

@router.post("/orders", response_model=Response, summary="提交周边预约")
async def create_merch_order(
    order_data: MerchOrderCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """保存用户预约周边的记录"""
    # 检查是否重复预约
    existing = db.query(MerchOrder).filter(
        MerchOrder.user_id == user_id,
        MerchOrder.product_id == order_data.product_id
    ).first()
    
    if existing:
        return Response(code=400, message="您已预约过该商品，不可重复预约")
        
    new_order = MerchOrder(
        user_id=user_id,
        product_id=order_data.product_id,
        product_name=order_data.product_name
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return Response(
        message="预约成功",
        data={"id": new_order.id}
    )

@router.get("/orders/my", response_model=Response, summary="获取我的所有周边预约")
async def get_my_merch_orders(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户拉取的周边预约列表"""
    orders = db.query(MerchOrder).filter(
        MerchOrder.user_id == user_id
    ).order_by(desc(MerchOrder.created_at)).all()
    
    return Response(
        message="获取成功",
        data={
            "count": len(orders),
            "orders": [{"id": o.id, "product_id": o.product_id, "product_name": o.product_name, "created_at": o.created_at} for o in orders]
        }
    )
