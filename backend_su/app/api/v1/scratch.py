"""
刮刮乐记录相关 API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.scratch import ScratchRecord
from app.schemas.common import Response
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/scratch", tags=["刮刮乐"])

class ScratchCreate(BaseModel):
    is_win: bool
    prize_name: str = None

class ScratchResponse(BaseModel):
    id: int
    user_id: int
    is_win: bool
    prize_name: str = None
    created_at: datetime
    
    class Config:
        orm_mode = True

@router.post("", response_model=Response, summary="保存刮刮乐结果")
async def create_scratch_record(
    scratch_data: ScratchCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    保存用户刮卡结果
    """
    new_record = ScratchRecord(
        user_id=user_id,
        is_win=scratch_data.is_win,
        prize_name=scratch_data.prize_name
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    return Response(
        message="记录保存成功",
        data={
            "id": new_record.id,
            "is_win": new_record.is_win,
            "prize_name": new_record.prize_name
        }
    )

@router.get("/my", response_model=Response, summary="获取我的刮刮乐中奖历史")
async def get_my_scratch_records(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的刮奖历史记录（中奖次数等）
    """
    records = db.query(ScratchRecord).filter(
        ScratchRecord.user_id == user_id,
        ScratchRecord.is_win == True
    ).order_by(ScratchRecord.created_at.desc()).all()
    
    return Response(
        message="获取成功",
        data={
            "win_count": len(records),
            "records": [{"prize_name": r.prize_name, "created_at": r.created_at} for r in records]
        }
    )
