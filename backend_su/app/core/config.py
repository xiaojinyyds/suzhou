"""
应用配置管理
"""
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """应用配置类"""
    # pydantic v2 配置：加载 .env，区分大小写，忽略未定义的额外环境变量（如 MAIL_*）
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=True,
        extra="ignore",
    )
    
    # 应用基础配置
    APP_NAME: str = Field(default="苏州石像打卡API", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=True, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # MySQL 数据库配置
    MYSQL_HOST: str = Field(default="localhost", env="MYSQL_HOST")
    MYSQL_PORT: int = Field(default=3306, env="MYSQL_PORT")
    MYSQL_USER: str = Field(default="root", env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(default="", env="MYSQL_PASSWORD")
    MYSQL_DATABASE: str = Field(default="suzhou_checkin", env="MYSQL_DATABASE")
    
    # Redis 配置
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: str = Field(default="", env="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # 阿里云 OSS 配置
    OSS_ACCESS_KEY_ID: str = Field(default="", env="OSS_ACCESS_KEY_ID")
    OSS_ACCESS_KEY_SECRET: str = Field(default="", env="OSS_ACCESS_KEY_SECRET")
    OSS_ENDPOINT: str = Field(default="oss-cn-shanghai.aliyuncs.com", env="OSS_ENDPOINT")
    OSS_BUCKET_NAME: str = Field(default="suzhou-checkin", env="OSS_BUCKET_NAME")
    OSS_BASE_URL: str = Field(default="", env="OSS_BASE_URL")
    # 可选：上传前缀、回调、过期时间
    OSS_FOLDER_PREFIX: str = Field(default="uploads", env="OSS_FOLDER_PREFIX")
    OSS_CALLBACK_URL: str = Field(default="", env="OSS_CALLBACK_URL")
    OSS_EXPIRE_TIME: int = Field(default=3600, env="OSS_EXPIRE_TIME")
    
    # 邮件配置（验证码发送）
    MAIL_HOST: str = Field(default="smtp.qq.com", env="MAIL_HOST")
    MAIL_PORT: int = Field(default=465, env="MAIL_PORT")
    MAIL_USERNAME: str = Field(default="", env="MAIL_USERNAME")
    MAIL_PASSWORD: str = Field(default="", env="MAIL_PASSWORD")
    MAIL_FROM: str = Field(default="", env="MAIL_FROM")
    MAIL_FROM_NAME: str = Field(default="苏州打卡", env="MAIL_FROM_NAME")
    MAIL_SSL_VERIFY: bool = Field(default=True, env="MAIL_SSL_VERIFY")
    
    # 验证码配置
    VERIFICATION_CODE_EXPIRE: int = Field(default=300, env="VERIFICATION_CODE_EXPIRE")
    VERIFICATION_CODE_LENGTH: int = Field(default=6, env="VERIFICATION_CODE_LENGTH")
    
    # JWT 配置
    JWT_SECRET_KEY: str = Field(default="change-me-in-production", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # 跨域配置
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp"],
        env="ALLOWED_EXTENSIONS"
    )

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_bool(cls, value):
        """兼容 shell 中的 DEBUG=release / debug 等非标准布尔值。"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug", "dev", "development"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "prod", "production"}:
                return False
        return value

    @field_validator("MAIL_SSL_VERIFY", mode="before")
    @classmethod
    def parse_mail_ssl_verify(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off"}:
                return False
        return value
    
    @property
    def DATABASE_URL(self) -> str:
        """生成数据库连接 URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    @property
    def REDIS_URL(self) -> str:
        """生成 Redis 连接 URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # 注意：Pydantic v2 已使用 model_config，不能再定义 class Config


# 创建全局配置实例
settings = Settings()
