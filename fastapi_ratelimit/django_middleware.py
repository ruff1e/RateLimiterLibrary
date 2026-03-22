from django.http import JsonResponse
from fastapi_ratelimit.backends.redis import RedisBackend
from fastapi_ratelimit.algorithms.fixed_window import fixed_window


class RateLimitMiddleware:
    def __init__(self, get_response, limit: int = 100, window: int = 60, algorithm=fixed_window, host="localhost", port=6379, db=0):
        self.get_response = get_response
        self.limit = limit
        self.window = window
        self.algorithm = algorithm
        self.backend = RedisBackend(host=host, port=port, db=db)

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        if not self.backend.is_allowed(key=ip, limit=self.limit, window=self.window, algorithm=self.algorithm):
            return JsonResponse(
                {"detail": "Rate Limit Exceeded"},
                status=429
            )

        return self.get_response(request)