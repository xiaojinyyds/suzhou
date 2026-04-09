"""
用户相关的 Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础 Schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None


class UserCreate(UserBase):
    """用户创建 Schema"""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """用户登录 Schema"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户响应 Schema"""
    id: int
    avatar_url: Optional[str] = None
    theme: Optional[str] = "wenchang"
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户更新 Schema"""
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    theme: Optional[str] = None


class TokenResponse(BaseModel):
    """Token 响应 Schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ===== 以下为参考项目对齐的认证请求模型 =====

class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    email: EmailStr = Field(..., description="邮箱地址")


class UserRegisterRequest(BaseModel):
    """用户注册请求（邮箱+验证码）"""
    email: EmailStr = Field(..., description="邮箱")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")


class UserLoginRequest(BaseModel):
    """用户登录请求（账号可以是用户名/邮箱/手机号）"""
    account: str = Field(..., description="账号（用户名/邮箱/手机号）")
    password: str = Field(..., description="密码")


class ForgotPasswordRequest(BaseModel):
    """忘记密码请求（发送验证码）"""
    email: EmailStr = Field(..., description="注册邮箱")


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    email: EmailStr = Field(..., description="邮箱")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, max_length=20, description="新密码")
