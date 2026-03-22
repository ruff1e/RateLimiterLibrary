import redis
from fastapi_ratelimit.algorithms.sliding_window import sliding_window


def test_sliding_window():

    client = redis.Redis(host="localhost", port=6379, db=0)
    client.delete("192.168.1.1")

    result = sliding_window(client = client, key = "192.168.1.1", limit =  100, window = 60)
    assert result == True


    for i in range(100):
        sliding_window(client = client, key = "192.168.1.1", limit =  100, window = 60)


    result = sliding_window(client = client, key = "192.168.1.1", limit =  100, window = 60)
    assert result == False
