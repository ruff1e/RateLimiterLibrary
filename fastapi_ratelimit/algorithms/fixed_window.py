import redis


def fixed_window(client: redis.Redis, key: str, limit: int, window: int) -> bool:

    # increment the key, if it doesnt exists, redis creates it and sets it to 1
    count = client.incr(key)

    # if the count is 1, it means it's the first request, so set a window(60 seconds usually) long timer to expire
    if count == 1:
        client.expire(key, window)
    
    # if the count goes over the limit, block the request
    if count > limit:
        return False


    #otherwise allow the request
    return True
