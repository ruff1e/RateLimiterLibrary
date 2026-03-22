import pytest
import redis
from django.conf import settings
from unittest.mock import MagicMock
from fastapi_ratelimit.django_middleware import RateLimitMiddleware
from fastapi_ratelimit.algorithms.fixed_window import fixed_window

if not settings.configured:
    settings.configure(DEFAULT_CHARSET="utf-8")


@pytest.fixture
def middleware():
    get_response = MagicMock(return_value="ok")
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.delete("192.168.1.1")
    return RateLimitMiddleware(
        get_response,
        limit=5,
        window=60,
        algorithm=fixed_window
    )


def make_request(ip="192.168.1.1"):
    request = MagicMock()
    request.META = {"REMOTE_ADDR": ip}
    return request


def test_requests_within_limit(middleware):
    for _ in range(5):
        response = middleware(make_request())
        assert response == "ok"


def test_request_over_limit(middleware):
    for _ in range(5):
        middleware(make_request())

    response = middleware(make_request())
    assert response.status_code == 429