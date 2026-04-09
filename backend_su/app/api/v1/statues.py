"""
石像景点相关 API
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.models.statue import Statue
from app.schemas.statue import StatueResponse
from app.schemas.common import Response

router = APIRouter(prefix="/statues", tags=["石像景点"])


def safe_json_loads(json_str: str) -> list:
    """安全地解析 JSON 字符串，失败时返回空列表"""
    if not json_str or json_str.strip() == "":
        return []
    try:
        result = json.loads(json_str)
        return result if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


@router.get("", response_model=Response[List[StatueResponse]], summary="获取石像列表")
async def get_statues(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """
    获取所有石像景点列表（仅返回启用的景点）
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    # 查询启用的景点，按排序序号排序
    statues = db.query(Statue).filter(
        Statue.is_active == True
    ).order_by(
        Statue.order_index, Statue.id
    ).offset(skip).limit(limit).all()
    
    # 构建响应数据
    response_data = [
        StatueResponse(
            id=s.id,
            name=s.name,
            icon=s.icon,
            latitude=s.latitude,
            longitude=s.longitude,
            radius=s.radius,
            introduction=s.introduction,
            history=s.history,
            cultural_value=s.cultural_value,
            images=safe_json_loads(s.images),
            order_index=s.order_index,
            is_active=s.is_active,
            is_checked=False,  # 需要结合用户打卡记录判断
            created_at=s.created_at
        )
        for s in statues
    ]
    
    return Response(message="获取成功", data=response_data)


@router.get("/{statue_id}", response_model=Response[StatueResponse], summary="获取石像详情")
async def get_statue(statue_id: int, db: Session = Depends(get_db)):
    """
    根据 ID 获取石像详情
    """
    # 查询景点
    statue = db.query(Statue).filter(Statue.id == statue_id).first()
    
    if not statue:
        raise HTTPException(status_code=404, detail="景点不存在")
    
    # 如果景点未启用，也返回 404
    if not statue.is_active:
        raise HTTPException(status_code=404, detail="景点不存在")
    
    # 构建响应数据
    response_data = StatueResponse(
        id=statue.id,
        name=statue.name,
        icon=statue.icon,
        latitude=statue.latitude,
        longitude=statue.longitude,
        radius=statue.radius,
        introduction=statue.introduction,
        history=statue.history,
        cultural_value=statue.cultural_value,
        images=safe_json_loads(statue.images),
        order_index=statue.order_index,
        is_active=statue.is_active,
        is_checked=False,  # 需要结合用户打卡记录判断
        created_at=statue.created_at
    )
    
    return Response(message="获取成功", data=response_data)


@router.get("/nearby", response_model=Response[List[StatueResponse]], summary="获取附近的石像")
async def get_nearby_statues(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius: int = Query(5000, ge=100, le=50000),
    db: Session = Depends(get_db)
):
    """
    根据当前位置获取附近的石像
    - **latitude**: 纬度
    - **longitude**: 经度
    - **radius**: 搜索半径（米，默认5000米）
    """
    import math
    
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
    
    # 查询所有启用的景点
    statues = db.query(Statue).filter(Statue.is_active == True).all()
    
    # 计算距离并过滤
    nearby_statues = []
    for statue in statues:
        distance = calculate_distance(latitude, longitude, statue.latitude, statue.longitude)
        if distance <= radius:
            nearby_statues.append((statue, distance))
    
    # 按距离排序
    nearby_statues.sort(key=lambda x: x[1])
    
    # 构建响应数据
    response_data = [
        StatueResponse(
            id=s.id,
            name=s.name,
            icon=s.icon,
            latitude=s.latitude,
            longitude=s.longitude,
            radius=s.radius,
            introduction=s.introduction,
            history=s.history,
            cultural_value=s.cultural_value,
            images=safe_json_loads(s.images),
            order_index=s.order_index,
            is_active=s.is_active,
            is_checked=False,
            distance=round(dist, 2),  # 保留两位小数
            created_at=s.created_at
        )
        for s, dist in nearby_statues
    ]
    
    return Response(message="获取成功", data=response_data)
