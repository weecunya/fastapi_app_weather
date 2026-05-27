from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/weather/")
    assert response.status_code == 200

def test_weather():
    response = client.get("/weather/city?city_name=moscow")
    assert response.status_code == 200