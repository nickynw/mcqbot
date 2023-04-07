"""Test the basic fastapi template"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    """Checks the api was able to run using a basic endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}
