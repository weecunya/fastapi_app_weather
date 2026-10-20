import pytest
import requests
from app.config import settings



@pytest.fixture
def token(data_register):
    requests.post(f'{settings.BASE_URL}/auth/register/', json=data_register)
    resp = requests.post(f'{settings.BASE_URL}/auth/login',json={"email": "wica@example.com" ,"password": "696969"})
    token = resp.cookies.get("session_id")
    return token

@pytest.fixture
def data_register():
    return {
    "email": "wica@example.com",
    "password": "696969",
    "password2": "696969",
    "first_name": "wica",
    "last_name": "szmak"
}