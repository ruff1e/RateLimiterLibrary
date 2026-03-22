# fastapi-ratelimit

A rate limiting library for FastAPI and Django using Redis with support for multiple algorithms.

## Features

- Three rate limiting algorithms: Fixed Window, Sliding Window, Token Bucket
- FastAPI decorator: apply rate limits per route
- FastAPI middleware: apply rate limits to all routes
- Django middleware support
- Redis backend

## Requirements

- Python 3.12+
- Redis server

## Installation

```bash
pip install fastapi django redis httpx
```

## Quick Start

### FastAPI — Decorator

Apply rate limiting to individual routes:

```python
from fastapi import FastAPI, Request
from fastapi_ratelimit.limiter import rate_limit
from fastapi_ratelimit.algorithms.sliding_window import sliding_window

app = FastAPI()

@app.get("/login")
@rate_limit(limit=5, window=60, algorithm=sliding_window)
async def login(request: Request):
    return {"message": "logged in"}
```

### FastAPI — Middleware

Apply rate limiting to all routes globally:

```python
from fastapi import FastAPI
from fastapi_ratelimit.middleware import RateLimitMiddleware
from fastapi_ratelimit.algorithms.fixed_window import fixed_window

app = FastAPI()

app.add_middleware(
    RateLimitMiddleware,
    limit=100,
    window=60,
    algorithm=fixed_window,
)
```

### Django — Middleware

In `settings.py`:

```python
MIDDLEWARE = [
    "fastapi_ratelimit.django_middleware.RateLimitMiddleware",
    # ...
]
```

For custom configuration, subclass it:

```python
# myapp/middleware.py
from fastapi_ratelimit.django_middleware import RateLimitMiddleware
from fastapi_ratelimit.algorithms.sliding_window import sliding_window

class MyRateLimiter(RateLimitMiddleware):
    def __init__(self, get_response):
        super().__init__(
            get_response,
            limit=50,
            window=60,
            algorithm=sliding_window,
        )
```

```python
# settings.py
MIDDLEWARE = [
    "myapp.middleware.MyRateLimiter",
]
```

## Algorithms

### Fixed Window
Counts requests in fixed time buckets. Simple and fast. Can allow bursts at window boundaries.

```python
from fastapi_ratelimit.algorithms.fixed_window import fixed_window
```

### Sliding Window
Tracks exact request timestamps in a rolling window. More accurate than fixed window, no boundary bursts.

```python
from fastapi_ratelimit.algorithms.sliding_window import sliding_window
```

### Token Bucket
Tokens refill gradually at a constant rate. Allows short bursts while enforcing an average rate.

```python
from fastapi_ratelimit.algorithms.token_bucket import token_bucket
```

## Configuration

| Parameter | Description | Default |
|---|---|---|
| `limit` | Max requests allowed | required |
| `window` | Time window in seconds | required |
| `algorithm` | Rate limiting algorithm | `fixed_window` |
| `host` | Redis host | `localhost` |
| `port` | Redis port | `6379` |
| `db` | Redis database index | `0` |

## Running Tests

Start Redis:

```bash
docker run -d --name redis -p 6379:6379 redis:latest
```

Run tests:

```bash
pytest tests/ -v
```

## Project Structure

```text
fastapi_ratelimit/
├── algorithms/
│   ├── fixed_window.py
│   ├── sliding_window.py
│   └── token_bucket.py
├── backends/
│   ├── base.py
│   └── redis.py
├── django_middleware.py
├── limiter.py
└── middleware.py
```
