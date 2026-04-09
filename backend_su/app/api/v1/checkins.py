"""
打卡记录相关 API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, date
import math
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.statue import Statue
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInCreate, CheckInResponse, CheckInResult
from app.schemas.common import Response

router = APIRouter(prefix="/checkins", tags=["打卡记录"])
MIN_CHECKIN_RADIUS_METERS = 10000


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    使用 Haversine 公式计算两点之间的距离（单位：米）
    """
    R = 6371000  # 地球半径，单位：米
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


@router.post("", response_model=Response[CheckInResult], summary="打卡")
async def create_checkin(
    checkin_data: CheckInCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    用户打卡接口
    - **statue_id**: 景点ID
    - **latitude**: 当前纬度
    - **longitude**: 当前经度
    
    返回打卡结果，包括是否成功、距离等信息
    """
    # 1. 验证用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 2. 获取景点信息
    statue = db.query(Statue).filter(Statue.id == checkin_data.statue_id).first()
    if not statue:
        raise HTTPException(status_code=404, detail="景点不存在")
    
    if not statue.is_active:
        raise HTTPException(status_code=400, detail="该景点暂不可打卡")
    
    # 3. 计算距离
    distance = calculate_distance(
        checkin_data.latitude,
        checkin_data.longitude,
        statue.latitude,
        statue.longitude
    )
    
    # 4. 判断是否在打卡范围内（业务口径统一为至少 10000 米）
    effective_radius = max(statue.radius or 0, MIN_CHECKIN_RADIUS_METERS)
    if distance > effective_radius:
        return Response(
            message=f"您距离景点 {round(distance, 2)} 米，超出打卡范围（{effective_radius}米）",
            data=CheckInResult(
                success=False,
                message=f"请靠近景点至 {effective_radius} 米范围内打卡",
                distance=round(distance, 2),
                checkin=None
            )
        )
    
    # 5. 检查今天是否已经打卡过
    today = date.today()
    existing_checkin = db.query(CheckIn).filter(
        and_(
            CheckIn.user_id == user_id,
            CheckIn.statue_id == checkin_data.statue_id,
            func.date(CheckIn.created_at) == today
        )
    ).first()
    
    if existing_checkin:
        return Response(
            message="今天已经打卡过了",
            data=CheckInResult(
                success=False,
                message="您今天已经在此景点打卡过了",
                distance=round(distance, 2),
                checkin=CheckInResponse(
                    id=existing_checkin.id,
                    user_id=existing_checkin.user_id,
                    statue_id=existing_checkin.statue_id,
                    latitude=existing_checkin.check_latitude,
                    longitude=existing_checkin.check_longitude,
                    distance=existing_checkin.distance,
                    created_at=existing_checkin.created_at
                )
            )
        )
    
    # 6. 保存打卡记录
    new_checkin = CheckIn(
        user_id=user_id,
        statue_id=checkin_data.statue_id,
        check_latitude=checkin_data.latitude,
        check_longitude=checkin_data.longitude,
        distance=round(distance, 2),
        is_valid=True
    )
    
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)
    
    return Response(
        message="打卡成功！🎉",
        data=CheckInResult(
            success=True,
            message=f"恭喜您成功打卡 {statue.name}",
            distance=round(distance, 2),
            checkin=CheckInResponse(
                id=new_checkin.id,
                user_id=new_checkin.user_id,
                statue_id=new_checkin.statue_id,
                latitude=new_checkin.check_latitude,
                longitude=new_checkin.check_longitude,
                distance=new_checkin.distance,
                created_at=new_checkin.created_at
            )
        )
    )


@router.get("/my", response_model=Response[List[CheckInResponse]], summary="获取我的打卡记录")
async def get_my_checkins(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有打卡记录
    """
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id
    ).order_by(CheckIn.created_at.desc()).all()
    
    response_data = [
        CheckInResponse(
            id=c.id,
            user_id=c.user_id,
            statue_id=c.statue_id,
            latitude=c.check_latitude,
            longitude=c.check_longitude,
            distance=c.distance,
            created_at=c.created_at
        )
        for c in checkins
    ]
    
    return Response(message="获取成功", data=response_data)


@router.get("/statistics", response_model=Response, summary="获取打卡统计")
async def get_checkin_statistics(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的打卡统计信息
    - 总打卡数
    - 已完成景点数
    - 完成率等
    """
    # 获取所有启用的景点总数
    total_statues = db.query(Statue).filter(Statue.is_active == True).count()
    
    # 获取用户打卡的不同景点数（去重）
    checked_statues = db.query(func.count(func.distinct(CheckIn.statue_id))).filter(
        CheckIn.user_id == user_id
    ).scalar() or 0
    
    # 获取总打卡次数
    total_checkins = db.query(CheckIn).filter(CheckIn.user_id == user_id).count()
    
    # 计算完成率
    completion_rate = round((checked_statues / total_statues * 100), 2) if total_statues > 0 else 0
    
    return Response(
        message="获取成功",
        data={
            "total_statues": total_statues,
            "checked_statues": checked_statues,
            "total_checkins": total_checkins,
            "completion_rate": completion_rate
        }
    )
