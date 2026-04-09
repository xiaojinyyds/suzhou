"""
打卡记录数据模型
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class CheckIn(Base):
    """打卡记录表"""
    __tablename__ = "check_ins"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    statue_id = Column(Integer, ForeignKey("statues.id"), nullable=False, index=True, comment="景点ID")
    check_latitude = Column(Float, nullable=False, comment="打卡时的纬度")
    check_longitude = Column(Float, nullable=False, comment="打卡时的经度")
    distance = Column(Float, nullable=True, comment="与景点的距离（米）")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    device_info = Column(String(255), nullable=True, comment="设备信息")
    is_valid = Column(Boolean, default=True, comment="是否有效打卡")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="打卡时间")
    
    # 关联关系
    user = relationship("User", backref="check_ins")
    statue = relationship("Statue", backref="check_ins")
