"""
地理距离计算工具
"""
import math


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    使用 Haversine 公式计算两个经纬度坐标之间的距离
    
    Args:
        lat1: 第一个点的纬度
        lon1: 第一个点的经度
        lat2: 第二个点的纬度
        lon2: 第二个点的经度
    
    Returns:
        两点之间的距离（米）
    """
    # 地球半径（米）
    R = 6371000
    
    # 转换为弧度
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine 公式
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 返回距离（米）
    distance = R * c
    
    return round(distance, 2)


def is_within_radius(
    user_lat: float,
    user_lon: float,
    target_lat: float,
    target_lon: float,
    radius: float
) -> tuple[bool, float]:
    """
    判断用户是否在目标点的半径范围内
    
    Args:
        user_lat: 用户纬度
        user_lon: 用户经度
        target_lat: 目标点纬度
        target_lon: 目标点经度
        radius: 半径（米）
    
    Returns:
        (是否在范围内, 实际距离)
    """
    distance = haversine_distance(user_lat, user_lon, target_lat, target_lon)
    is_within = distance <= radius
    
    return is_within, distance
