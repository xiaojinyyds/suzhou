"""
订单处理工具函数
"""
import random
import string
from datetime import datetime


def generate_order_no() -> str:
    """
    生成唯一的订单号
    格式: SZ + 年月日 + 时分秒 + 4位随机数
    示例: SZ20241116145230ABCD
    
    Returns:
        订单号字符串
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    order_no = f"SZ{timestamp}{random_str}"
    
    return order_no


def calculate_shipping_fee(total_amount: float) -> float:
    """
    计算配送费
    规则：
    - 满50元免配送费
    - 不满50元收取5元配送费
    
    Args:
        total_amount: 商品总额
    
    Returns:
        配送费
    """
    if total_amount >= 50:
        return 0.0
    else:
        return 5.0


def calculate_discount(total_amount: float, user_level: str = "normal") -> float:
    """
    计算优惠金额
    规则示例：
    - 普通用户：满100减10
    - VIP用户：满100减20
    
    Args:
        total_amount: 商品总额
        user_level: 用户等级
    
    Returns:
        优惠金额
    """
    if total_amount < 100:
        return 0.0
    
    if user_level == "vip":
        return 20.0
    else:
        return 10.0
