from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi_ratelimit.backends.redis import RedisBackend
from fastapi_ratelimit.algorithms.fixed_window import fixed_window


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int, window: int, algorithm=fixed_window, host="localhost", port=6379, db=0):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.algorithm = algorithm
        self.backend = RedisBackend(host=host, port=port, db=db)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host

        if not self.backend.is_allowed(key=ip, limit=self.limit, window=self.window, algorithm=self.algorithm):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate Limit Exceeded"},
            )

        return await call_next(request)
    