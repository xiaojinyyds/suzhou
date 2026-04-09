"""
合成大狸猫战绩表
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class MergeGameRecord(Base):
    """合成游戏战绩"""
    __tablename__ = "merge_game_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    score = Column(Integer, default=0, nullable=False, comment="本局最终得分")
    max_combo = Column(Integer, default=0, nullable=True, comment="最大连击数")
    highest_level = Column(Integer, default=0, nullable=True, comment="合成出的最高等级狸猫(0-6)")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="游戏时间")
    
    # 关联关系
    user = relationship("User", backref="merge_game_records")
