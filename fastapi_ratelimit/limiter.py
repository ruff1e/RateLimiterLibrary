from fastapi_ratelimit.backends.redis import RedisBackend
from fastapi_ratelimit.algorithms.fixed_window import fixed_window
from fastapi import Request, HTTPException
import functools



def rate_limit(limit: int, window: int, algorithm=fixed_window, host="localhost", port=6379, db=0):
    backend = RedisBackend(host=host, port=port, db=db)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, **kwargs):
            ip = request.client.host

            if not backend.is_allowed(key=ip, limit=limit, window=window, algorithm=algorithm):
                raise HTTPException(status_code=429, detail="Rate Limit Exceeded")

            return await func(request, **kwargs)
        return wrapper
    return decorator
