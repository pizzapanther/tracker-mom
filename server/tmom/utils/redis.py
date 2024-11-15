from functools import cache

import redis

from django.conf import settings


@cache
def client():
  return redis.Redis.from_url(f"{settings.REDIS_URL}/2")
