import redis
from fastapi_ratelimit.algorithms.fixed_window import fixed_window


def test_fixed_window():

    client = redis.Redis(host="localhost", port=6379, db=0)
    client.delete("192.168.1.1")

    result = fixed_window(client = client, key = "192.168.1.1", limit =  100, window = 60)
    assert result == True

    
    for i in range(99):
        fixed_window(client = client, key = "192.168.1.1", limit =  100, window = 60)
    

    result = fixed_window(client = client, key = "192.168.1.1", limit =  100, window = 60)
    assert result == False
