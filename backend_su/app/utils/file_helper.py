"""
文件处理工具函数
"""
import os
import uuid
from datetime import datetime
from typing import Optional
from app.core.config import settings


def generate_unique_filename(original_filename: str) -> str:
    """
    生成唯一的文件名
    
    Args:
        original_filename: 原始文件名
    
    Returns:
        唯一的文件名
    """
    # 获取文件扩展名
    _, ext = os.path.splitext(original_filename)
    
    # 生成时间戳 + UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    
    # 组合新文件名
    new_filename = f"{timestamp}_{unique_id}{ext}"
    
    return new_filename


def validate_file_extension(filename: str, allowed_extensions: list = None) -> bool:
    """
    验证文件扩展名是否合法
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名列表
    
    Returns:
        是否合法
    """
    if allowed_extensions is None:
        allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    return ext in allowed_extensions


def validate_file_size(file_size: int, max_size: int = None) -> bool:
    """
    验证文件大小是否合法
    
    Args:
        file_size: 文件大小（字节）
        max_size: 最大允许大小（字节）
    
    Returns:
        是否合法
    """
    if max_size is None:
        max_size = settings.MAX_UPLOAD_SIZE
    
    return file_size <= max_size


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小显示
    
    Args:
        size_bytes: 文件大小（字节）
    
    Returns:
        格式化后的字符串（如 "2.5 MB"）
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
