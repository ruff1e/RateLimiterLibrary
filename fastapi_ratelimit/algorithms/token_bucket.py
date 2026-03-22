import redis
import time


def token_bucket(client: redis.Redis, key: str, capacity: int, refill_rate: float, window: int) -> bool:

    now = time.time()
    # returns a float like 1700000000.0

    bucket = client.hgetall(key)
    # returns a dict like {b"tokens": b"5.0", b"last_refill": b"1700000000.0"}
    # also it returns bytes

    if not bucket:
    # first time this user is seen, initialize their bucket
        client.hset(key, mapping={"tokens": capacity - 1, "last_refill": now})
        return True

    last_refill = float(bucket[b"last_refill"])
    current_tokens = float(bucket[b"tokens"])

    elapsed = now - last_refill
    tokens_to_add = elapsed * refill_rate

    new_tokens = min(capacity, current_tokens + tokens_to_add)

    
    if current_tokens < 1 :
        return False


    client.hset(key, mapping={"tokens": new_tokens - 1, "last_refill": now})


    return True