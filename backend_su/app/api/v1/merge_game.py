"""
合成狸猫游戏 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.merge_game import MergeGameRecord
from app.schemas.common import Response
from pydantic import BaseModel

router = APIRouter(prefix="/merge-game", tags=["合成小狸猫"])

class MergeGameCreate(BaseModel):
    score: int
    max_combo: Optional[int] = 0
    highest_level: Optional[int] = 0

@router.post("", response_model=Response, summary="保存游戏战绩")
async def save_merge_game_record(
    game_data: MergeGameCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """保存玩家当局战绩"""
    new_record = MergeGameRecord(
        user_id=user_id,
        score=game_data.score,
        max_combo=game_data.max_combo,
        highest_level=game_data.highest_level
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    # 获取提交后的用户最高分
    max_score = db.query(func.max(MergeGameRecord.score)).filter(
        MergeGameRecord.user_id == user_id
    ).scalar() or 0
    
    return Response(
        message="战绩保存成功",
        data={
            "id": new_record.id,
            "max_score": max_score
        }
    )

@router.get("/my", response_model=Response, summary="获取我的最高分")
async def get_my_highest_score(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取当前用户的历史最高分"""
    max_score = db.query(func.max(MergeGameRecord.score)).filter(
        MergeGameRecord.user_id == user_id
    ).scalar() or 0
    
    return Response(
        message="获取成功",
        data={
            "high_score": max_score
        }
    )
