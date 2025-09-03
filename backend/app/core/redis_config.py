"""Redis configuration for background job processing."""
import os
from typing import Optional
import redis
from rq import Queue


class RedisConfig:
    """Redis connection and queue configuration."""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.connection: Optional[redis.Redis] = None
        self.queue: Optional[Queue] = None
    
    def get_connection(self) -> redis.Redis:
        """Get Redis connection, creating if needed."""
        if self.connection is None:
            try:
                self.connection = redis.from_url(self.redis_url)
                # Test connection
                self.connection.ping()
            except redis.ConnectionError:
                # Fallback for development without Redis
                print("⚠️ Redis not available, using mock connection")
                self.connection = MockRedis()
        return self.connection
    
    def get_queue(self, name: str = 'default') -> Queue:
        """Get RQ queue for job processing."""
        if self.queue is None:
            connection = self.get_connection()
            self.queue = Queue(name, connection=connection)
        return self.queue


class MockRedis:
    """Mock Redis for development without Redis server."""
    
    def ping(self):
        return True
    
    def set(self, key, value, **kwargs):
        return True
    
    def get(self, key):
        return None
    
    def delete(self, key):
        return True


# Global instance
redis_config = RedisConfig()
