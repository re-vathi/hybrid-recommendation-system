import redis

cache = redis.Redis(
    host="localhost",
    port=5342,
    decode_responses=True
)