"""
刮刮乐记录数据模型
"""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScratchRecord(Base):
    """刮刮乐记录表"""
    __tablename__ = "scratch_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    is_win = Column(Boolean, default=False, nullable=False, comment="是否中奖")
    prize_name = Column(String(50), nullable=True, comment="奖品名称/狸猫名")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="刮卡时间")
    
    # 关联关系
    user = relationship("User", backref="scratch_records")
