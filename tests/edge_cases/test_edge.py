import pytest
import requests

from app.config import settings


def test_update_empty_data(token):
    response = requests.put(f"{settings.BASE_URL}/users/update",cookies={"session_id":token},json={"first_name":"","last_name":""})
    assert response.status_code == 200


def test_delete_twice(token):
    requests.delete(f"{settings.BASE_URL}/users/delete", cookies={"session_id": token})
    response = requests.delete(f"{settings.BASE_URL}/users/delete", cookies={"session_id":token})
    assert response.status_code == 400

def test_invalid_endpoint():
    resp = requests.get(f"{settings.BASE_URL}/users/download",json={"first_name": "wica"})
    assert resp.status_code == 404