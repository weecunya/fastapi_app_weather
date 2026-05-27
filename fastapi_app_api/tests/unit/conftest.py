

import pytest




@pytest.fixture
def data_register():
    return {
    "email": "wica@example.com",
    "password": "696969",
    "password2": "696969",
    "first_name": "wica",
    "last_name": "szmak"
}



@pytest.fixture
def data_register_for_login():
    return {
    "email": "wicunya@example.com",
    "password": "696969",
    "password2": "696969",
    "first_name": "wicunya",
    "last_name": "szmakowizer"
}


