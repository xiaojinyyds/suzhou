"""
阿里云 OSS 客户端配置
"""
import oss2
from typing import Optional
from datetime import datetime
from app.core.config import settings
import uuid
from pathlib import Path


class OSSClient:
    """阿里云 OSS 客户端封装类"""
    
    def __init__(self):
        """初始化OSS客户端"""
        self.auth: Optional[oss2.Auth] = None
        self.bucket: Optional[oss2.Bucket] = None
        self.domain: Optional[str] = None
    
    def connect(self):
        """初始化 OSS 连接"""
        try:
            # 创建认证对象
            self.auth = oss2.Auth(
                settings.OSS_ACCESS_KEY_ID,
                settings.OSS_ACCESS_KEY_SECRET
            )
            
            # 创建 Bucket 对象
            self.bucket = oss2.Bucket(
                self.auth,
                settings.OSS_ENDPOINT,
                settings.OSS_BUCKET_NAME
            )
            
            # 设置域名
            self.domain = settings.OSS_BASE_URL or f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}"
            
            print("✅ 阿里云 OSS 客户端初始化成功")
            
        except Exception as e:
            print(f"❌ 阿里云 OSS 客户端初始化失败: {str(e)}")
            self.bucket = None
    
    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        folder: str = "uploads"
    ) -> Optional[dict]:
        """
        上传文件到 OSS
        
        Args:
            file_content: 文件内容（字节）
            filename: 原始文件名
            folder: 存储文件夹
            
        Returns:
            {
                'url': 'https://xxx.oss-cn-shanghai.aliyuncs.com/uploads/xxx.jpg',
                'key': 'uploads/xxx.jpg',
                'size': 12345
            }
        """
        if not self.bucket:
            return None
        
        try:
            # 生成唯一文件名
            file_ext = Path(filename).suffix.lower()
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            
            # OSS对象键（路径）
            object_key = f"{folder}/{datetime.now().strftime('%Y%m%d')}/{unique_filename}"
            
            # 上传到OSS
            result = self.bucket.put_object(object_key, file_content)
            
            if result.status != 200:
                raise Exception(f"上传失败: {result.status}")
            
            # 构建访问URL
            file_url = f"{self.domain}/{object_key}"
            
            return {
                'url': file_url,
                'key': object_key,
                'size': len(file_content)
            }
            
        except Exception as e:
            print(f"OSS 上传失败: {str(e)}")
            return None
    
    def delete_file(self, object_key: str) -> bool:
        """
        删除 OSS 上的文件
        
        Args:
            object_key: 文件路径
            
        Returns:
            成功返回 True，失败返回 False
        """
        if not self.bucket:
            return False
        
        try:
            result = self.bucket.delete_object(object_key)
            return result.status == 204
        except Exception as e:
            print(f"OSS 删除失败: {str(e)}")
            return False
    
    def get_bucket(self) -> Optional[oss2.Bucket]:
        """获取 Bucket 实例"""
        return self.bucket


# 创建全局 OSS 客户端实例
oss_client = OSSClient()


def get_oss() -> Optional[oss2.Bucket]:
    """
    获取 OSS Bucket 的依赖注入函数
    """
    return oss_client.get_bucket()
