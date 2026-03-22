from fastapi_ratelimit.backends.redis import RedisBackend
from fastapi_ratelimit.algorithms.fixed_window import fixed_window
from fastapi import Request, HTTPException





def rate_limit(limit: int, window: int):
    def decorator(func):
        async def wrapper(request: Request, **kwargs):
            
            host = request.client.host
            backend = RedisBackend(host=host, port=6379, db=0)

            if not backend.is_allowed(key=host, limit=limit, window=window, algorithm=fixed_window):
                raise HTTPException(
                    status_code=429,
                    detail="Rate Limit Exceeded"
                )


            return await func(request, **kwargs)
        return wrapper
    return decorator
