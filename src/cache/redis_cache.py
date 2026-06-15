import redis
import json
import os
from typing import Optional, Any
from src.utils.logger import logger

class RedisCache:
    def __init__(self, url: str = None):
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = None
        self.memory_cache = {}
        
        try:
            self.client = redis.from_url(self.url, decode_responses=True)
            self.client.ping()
            logger.info("✓ Redis connected")
        except Exception as e:
            logger.warning(f"⚠️ Redis unavailable, using in-memory cache")
            self.client = None
    
    def get(self, key: str) -> Optional[Any]:
        try:
            if self.client:
                data = self.client.get(key)
                if data:
                    return json.loads(data)
            return self.memory_cache.get(key)
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        try:
            data = json.dumps(value)
            if self.client:
                self.client.setex(key, ttl, data)
            self.memory_cache[key] = value
        except Exception:
            pass
    
    def clear(self):
        try:
            if self.client:
                self.client.flushdb()
            self.memory_cache.clear()
        except Exception:
            pass

cache = RedisCache()
