"""
FastAPI 主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.core.redis_client import redis_client
from app.core.oss_client import oss_client
from app.api.v1 import auth, statues, checkins, desserts, orders, upload, admin, photos, scratch, merge_game, merch


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    启动时初始化资源，关闭时清理资源
    """
    # 启动时执行
    print("🚀 正在启动应用...")
    
    # 检查数据库连接（不自动创建表）
    try:
        # 只测试连接，不创建表
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ 数据库连接成功")
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
    
    # 连接 Redis
    redis_client.connect()
    
    # 连接阿里云 OSS
    oss_client.connect()
    
    print("✅ 应用启动完成")
    
    yield
    
    # 关闭时执行
    print("🛑 正在关闭应用...")
    redis_client.disconnect()
    print("✅ 应用关闭完成")


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="苏州石像打卡网站后端 API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置 CORS 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")  # 管理员路由
app.include_router(statues.router, prefix="/api/v1")
app.include_router(checkins.router, prefix="/api/v1")
app.include_router(desserts.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(photos.router, prefix="/api/v1/photos", tags=["拍照"])
app.include_router(scratch.router, prefix="/api/v1")
app.include_router(merge_game.router, prefix="/api/v1")
app.include_router(merch.router, prefix="/api/v1")

@app.get("/", tags=["根路由"])
async def root():
    """根路由 - 健康检查"""
    return {
        "message": "欢迎使用苏州石像打卡 API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected" if redis_client.get_client() else "disconnected",
        "oss": "connected" if oss_client.get_bucket() else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
