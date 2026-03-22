import pytest
import redis
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi_ratelimit.limiter import rate_limit
from fastapi_ratelimit.algorithms.fixed_window import fixed_window


@pytest.fixture
def client():
    app = FastAPI()

    @app.get("/test")
    @rate_limit(limit=5, window=60, algorithm=fixed_window)
    async def test_route(request: Request):
        return {"message": "ok"}

    r = redis.Redis(host="localhost", port=6379, db=0)
    r.flushdb()

    return TestClient(app)


def test_requests_within_limit(client):
    for _ in range(5):
        response = client.get("/test")
        assert response.status_code == 200


def test_request_over_limit(client):
    for _ in range(5):
        client.get("/test")

    response = client.get("/test")
    assert response.status_code == 429
    assert response.json() == {"detail": "Rate Limit Exceeded"}