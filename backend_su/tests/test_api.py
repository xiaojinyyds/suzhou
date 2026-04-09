"""
API 测试示例
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """测试根路由"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"


def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# TODO: 添加更多测试用例
# - 用户注册测试
# - 用户登录测试
# - 打卡功能测试
# - 订单创建测试
# 等等...
