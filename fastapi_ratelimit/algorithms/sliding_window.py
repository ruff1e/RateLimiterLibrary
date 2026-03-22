import redis
import time
import uuid

def sliding_window(client: redis.Redis, key: str, limit: int, window: int) -> bool:

    #get the current time and set it to currTime (for example 17000100)
    currTime = time.time()

    #then get rid off all the requests older than 17000100-window
    # for example if the window is 60 seconds, remove everything between 0 and 17000040
    client.zremrangebyscore(key, 0, currTime-window)

    #then count the requests in the list
    count = client.zcard(key)

    #then if the count is over the limit, reject it
    if count > limit:
        return False
    

    # if not it means it is acceptable so add it to the list
    client.zadd(key, {str(uuid.uuid4()): currTime})

    return True
