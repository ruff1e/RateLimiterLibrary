import redis
from fastapi_ratelimit.algorithms.token_bucket import token_bucket


def test_token_bucket():

    client = redis.Redis(host="localhost", db=0)
    client.delete("192.168.1.1")


    result = token_bucket(client=client, key= "192.168.1.1", capacity= 10, refill_rate= 1.0, window= 60)
    assert result == True

    for i in range(9):
        token_bucket(client=client, key= "192.168.1.1", capacity= 10, refill_rate= 1.0, window= 60)


    result = token_bucket(client=client, key= "192.168.1.1", capacity= 10, refill_rate= 1.0, window= 60)

    assert result == False
