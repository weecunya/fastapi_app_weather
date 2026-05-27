import pytest
from fastapi.testclient import TestClient

from app.config import settings

import requests as client

from app.schemas import MessageResponse


@pytest.fixture
def token(data_register):
    client.post(f'{settings.BASE_URL}/auth/register/', json=data_register)
    resp = client.post(f'{settings.BASE_URL}/auth/login',json={"email": "wica@example.com" ,"password": "696969"})
    token = resp.cookies.get("session_id")
    return token


def test_me(data_register, token):
    response = client.get(f'{settings.BASE_URL}/users/me',cookies={"session_id":token})
    assert response.status_code == 200


def test_update_me(token):
    response = client.put(f'{settings.BASE_URL}/users/update',json={'first_name': 'wica',"last_name": "szmak"},cookies = {"session_id":token})
    assert response.status_code == 200
    assert MessageResponse(**response.json())

def test_delete_me(token):
    response = client.delete(f'{settings.BASE_URL}/users/delete',cookies={"session_id":token})
    assert response.status_code == 200
    assert MessageResponse(**response.json())


