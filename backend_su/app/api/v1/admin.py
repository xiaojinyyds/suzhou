"""
管理员API - 景点管理
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.statue import Statue
from app.schemas.statue import StatueCreate, StatueUpdate, StatueResponse
from app.schemas.common import Response

router = APIRouter(prefix="/admin/statues", tags=["管理员-景点管理"])


def verify_admin(user_id: int, db: Session):
    """验证用户是否为管理员"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )


def safe_json_loads(json_str: str) -> list:
    """安全地解析 JSON 字符串，失败时返回空列表"""
    if not json_str or json_str.strip() == "":
        return []
    try:
        result = json.loads(json_str)
        return result if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


@router.post("", response_model=Response[StatueResponse], summary="创建景点")
async def create_statue(
    statue_data: StatueCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    创建新的石像景点（仅管理员）
    
    - **name**: 景点名称（必填）
    - **latitude**: 纬度（必填）
    - **longitude**: 经度（必填）
    - **radius**: 打卡半径（米，默认100）
    - **introduction**: 景点简介
    - **history**: 历史背景
    - **cultural_value**: 文化价值
    - **images**: 图片URL列表
    - **icon**: emoji图标
    - **order_index**: 排序序号
    """
    verify_admin(user_id, db)
    
    # 检查景点名称是否已存在
    existing = db.query(Statue).filter(Statue.name == statue_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"景点 '{statue_data.name}' 已存在"
        )
    
    # 创建景点
    new_statue = Statue(
        name=statue_data.name,
        icon=statue_data.icon,
        latitude=statue_data.latitude,
        longitude=statue_data.longitude,
        radius=statue_data.radius,
        introduction=statue_data.introduction,
        history=statue_data.history,
        cultural_value=statue_data.cultural_value,
        images=json.dumps(statue_data.images) if statue_data.images else "[]",
        order_index=statue_data.order_index,
        is_active=True
    )
    
    db.add(new_statue)
    db.commit()
    db.refresh(new_statue)
    
    # 构造响应
    response_data = StatueResponse(
        id=new_statue.id,
        name=new_statue.name,
        icon=new_statue.icon,
        latitude=new_statue.latitude,
        longitude=new_statue.longitude,
        radius=new_statue.radius,
        introduction=new_statue.introduction,
        history=new_statue.history,
        cultural_value=new_statue.cultural_value,
        images=safe_json_loads(new_statue.images),
        order_index=new_statue.order_index,
        is_active=new_statue.is_active,
        is_checked=False,
        created_at=new_statue.created_at
    )
    
    return Response(message="景点创建成功", data=response_data)


@router.get("", response_model=Response[List[StatueResponse]], summary="获取所有景点（含禁用）")
async def get_all_statues(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取所有景点列表，包括已禁用的（仅管理员）
    """
    verify_admin(user_id, db)
    
    statues = db.query(Statue).order_by(Statue.order_index, Statue.id).offset(skip).limit(limit).all()
    
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
            created_at=s.created_at
        )
        for s in statues
    ]
    
    return Response(message="获取成功", data=response_data)


@router.get("/{statue_id}", response_model=Response[StatueResponse], summary="获取景点详情")
async def get_statue_detail(
    statue_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取指定景点的详细信息（仅管理员）
    """
    verify_admin(user_id, db)
    
    statue = db.query(Statue).filter(Statue.id == statue_id).first()
    if not statue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点不存在"
        )
    
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
        images=json.loads(statue.images) if statue.images else [],
        order_index=statue.order_index,
        is_active=statue.is_active,
        is_checked=False,
        created_at=statue.created_at
    )
    
    return Response(message="获取成功", data=response_data)


@router.put("/{statue_id}", response_model=Response[StatueResponse], summary="更新景点信息")
async def update_statue(
    statue_id: int,
    statue_data: StatueUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    更新景点信息（仅管理员）
    
    可以部分更新，只传需要更新的字段即可
    """
    verify_admin(user_id, db)
    
    statue = db.query(Statue).filter(Statue.id == statue_id).first()
    if not statue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点不存在"
        )
    
    # 如果更新名称，检查是否重复
    if statue_data.name and statue_data.name != statue.name:
        existing = db.query(Statue).filter(
            Statue.name == statue_data.name,
            Statue.id != statue_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"景点名称 '{statue_data.name}' 已被使用"
            )
    
    # 更新字段
    update_data = statue_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "images" and value is not None:
            setattr(statue, field, json.dumps(value))
        else:
            setattr(statue, field, value)
    
    db.commit()
    db.refresh(statue)
    
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
        images=json.loads(statue.images) if statue.images else [],
        order_index=statue.order_index,
        is_active=statue.is_active,
        is_checked=False,
        created_at=statue.created_at
    )
    
    return Response(message="更新成功", data=response_data)


@router.delete("/{statue_id}", response_model=Response, summary="删除景点")
async def delete_statue(
    statue_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    删除景点（仅管理员）
    
    注意：这是硬删除，会同时删除相关的打卡记录
    """
    verify_admin(user_id, db)
    
    statue = db.query(Statue).filter(Statue.id == statue_id).first()
    if not statue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点不存在"
        )
    
    db.delete(statue)
    db.commit()
    
    return Response(message=f"景点 '{statue.name}' 已删除")


@router.patch("/{statue_id}/toggle", response_model=Response[StatueResponse], summary="启用/禁用景点")
async def toggle_statue_status(
    statue_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    切换景点的启用/禁用状态（仅管理员）
    """
    verify_admin(user_id, db)
    
    statue = db.query(Statue).filter(Statue.id == statue_id).first()
    if not statue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点不存在"
        )
    
    # 切换状态
    statue.is_active = not statue.is_active
    db.commit()
    db.refresh(statue)
    
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
        images=json.loads(statue.images) if statue.images else [],
        order_index=statue.order_index,
        is_active=statue.is_active,
        is_checked=False,
        created_at=statue.created_at
    )
    
    status_text = "启用" if statue.is_active else "禁用"
    return Response(message=f"景点已{status_text}", data=response_data)


@router.post("/batch-update-order", response_model=Response, summary="批量更新景点排序")
async def batch_update_order(
    order_list: List[dict],  # [{"id": 1, "order_index": 0}, ...]
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    批量更新景点的排序序号（仅管理员）
    
    传入格式：[{"id": 1, "order_index": 0}, {"id": 2, "order_index": 1}, ...]
    """
    verify_admin(user_id, db)
    
    for item in order_list:
        statue_id = item.get("id")
        order_index = item.get("order_index")
        
        if statue_id is None or order_index is None:
            continue
        
        statue = db.query(Statue).filter(Statue.id == statue_id).first()
        if statue:
            statue.order_index = order_index
    
    db.commit()
    
    return Response(message="排序更新成功")
