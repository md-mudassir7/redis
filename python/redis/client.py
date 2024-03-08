import redis
from config.config import Settings
from utils.logger import logging

class RedisClient:
    settings = Settings.get_settings()
    
    client = redis.Redis(
        host = settings.redis_host,
        port = settings.redis_port,
        db = 0
    )
    
    @classmethod
    def get_redis_client(cls):
        """ get redis client """
        logging.info(f"Returning redis client instance")
        return RedisClient.client