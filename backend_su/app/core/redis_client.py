"""
Redis 连接配置
"""
import redis
import time
from typing import Optional
from redis import connection as redis_connection
from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError
from app.core.config import settings

# 某些 Windows/Python 环境下 redis-py 5.x 会出现
# HIREDIS_PACK_AVAILABLE=True 但 hiredis 符号未绑定，导致 AUTH/PING 时 NameError。
# 这里统一禁用 hiredis packer/parser，强制走纯 Python 实现，优先保证稳定性。
redis_connection.HIREDIS_AVAILABLE = False
redis_connection.HIREDIS_PACK_AVAILABLE = False


class RedisClient:
    """Redis 客户端封装类"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self._memory_store: dict[str, tuple[str, float]] = {}
    
    def connect(self):
        """建立 Redis 连接"""
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                socket_keepalive=True,
                health_check_interval=30,
                parser_class=redis_connection.DefaultParser,
            )
            # 测试连接
            self.client.ping()
            print("✅ Redis 连接成功")
        except Exception as e:
            print(f"❌ Redis 连接失败: {str(e)}")
            self.client = None
    
    def disconnect(self):
        """关闭 Redis 连接"""
        if self.client:
            self.client.close()
            print("Redis 连接已关闭")
    
    def get_client(self) -> Optional[redis.Redis]:
        """获取 Redis 客户端实例"""
        return self.client

    # 便捷方法：自动重连与错误兜底
    def _ensure(self) -> Optional[redis.Redis]:
        if self.client is None:
            self.connect()
        return self.client

    def get(self, key: str) -> Optional[str]:
        cli = self._ensure()
        if cli is None:
            return self._memory_get(key)
        try:
            return cli.get(key)
        except (RedisConnectionError, RedisTimeoutError):
            # 尝试重连一次
            self.connect()
            cli = self.client
            return cli.get(key) if cli else self._memory_get(key)
        except Exception:
            return self._memory_get(key)

    def set(self, key: str, value: str, expire: int = 300) -> bool:
        cli = self._ensure()
        if cli is None:
            return self._memory_set(key, value, expire)
        try:
            cli.setex(key, expire, value)
            return True
        except (RedisConnectionError, RedisTimeoutError):
            self.connect()
            cli = self.client
            if cli is None:
                return self._memory_set(key, value, expire)
            cli.setex(key, expire, value)
            return True
        except Exception:
            return self._memory_set(key, value, expire)

    def delete(self, key: str) -> bool:
        cli = self._ensure()
        if cli is None:
            return self._memory_delete(key)
        try:
            cli.delete(key)
            return True
        except (RedisConnectionError, RedisTimeoutError):
            self.connect()
            cli = self.client
            if cli is None:
                return self._memory_delete(key)
            cli.delete(key)
            return True
        except Exception:
            return self._memory_delete(key)

    def _memory_get(self, key: str) -> Optional[str]:
        item = self._memory_store.get(key)
        if not item:
            return None
        value, expire_at = item
        if expire_at < time.time():
            self._memory_store.pop(key, None)
            return None
        return value

    def _memory_set(self, key: str, value: str, expire: int = 300) -> bool:
        self._memory_store[key] = (value, time.time() + expire)
        print(f"⚠️ Redis 不可用，已回退到内存验证码缓存: {key}")
        return True

    def _memory_delete(self, key: str) -> bool:
        self._memory_store.pop(key, None)
        return True


# 创建全局 Redis 客户端实例
redis_client = RedisClient()


def get_redis() -> Optional[redis.Redis]:
    """
    获取 Redis 客户端的依赖注入函数
    """
    return redis_client.get_client()
