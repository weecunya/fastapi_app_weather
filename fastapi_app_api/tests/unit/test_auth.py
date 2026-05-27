


import requests as client

from app.config import settings


def test_register(data_register):
    response = client.post(f"{settings.BASE_URL}/auth/register", json=data_register)
    resp = client.post(f"{settings.BASE_URL}/auth/register", json=data_register)
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
    assert resp.status_code == 400
    assert resp.json() == {"detail": "User already exists"}


def test_login(data_register_for_login):
    client.post(f"{settings.BASE_URL}/auth/register", json=data_register_for_login)
    response = client.post(f"{settings.BASE_URL}/auth/login", json={"email": "wicunya@example.com", "password": "696969"})
    assert response.status_code == 200
    assert response.json() == {"status": "logged in"}

def test_fail_login():
    response = client.post(f"{settings.BASE_URL}/auth/login", json={})
    resp = client.post(f"{settings.BASE_URL}/auth/login", json={"email": "wicunya@hehe.com", "password": "676767"})
    response_fail_pass = client.post(f"{settings.BASE_URL}/auth/login", json={"email": "wica@example.com", "password": "676767"})
    assert response.status_code == 422
    assert resp.status_code == 401
    assert resp.json() == {"detail": 'User does not exist'}
    assert response_fail_pass.status_code == 400
    assert response_fail_pass.json() == {"detail": 'Incorrect password'}
