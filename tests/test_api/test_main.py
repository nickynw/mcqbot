"""Test the basic fastapi template"""

from api.main import api
from fastapi.testclient import TestClient

client = TestClient(api)


def test_live():
    """Checks the api was able to run using a basic endpoint"""
    response = client.get('/live')
    assert response.status_code == 200
    assert response.json() == {}


def test_root():
    """Checks the api was able to generate an mcq"""
    response = client.get('/')
    assert response.status_code == 200


def test_rate_limit():
    """Checks that rate limitation is occuring on the root endpoint"""
    # Send 5 requests to the rate-limited endpoint
    for _ in range(4):
        response = client.get('/')
        assert response.status_code == 200

    # The 6th request should exceed the rate limit and return a 429 error
    response = client.get('/')
    assert response.status_code == 429
