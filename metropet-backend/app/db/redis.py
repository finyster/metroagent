#metropet-backend/app/db/redis.py
import os
import redis.asyncio as redis

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')

redis_client = redis.from_url(REDIS_URL, decode_responses=True)
