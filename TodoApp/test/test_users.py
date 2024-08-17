from .utils import client, user_admin
from fastapi import status


def test_get_user(user_admin):
    response = client.get("/user/1")
    assert response.status_code == status.HTTP_200_OK

    assert response.json()["username"] == "admin"
    assert response.json()["email"] == "admin@admin.com"
    assert response.json()["username"] == "admin"
    assert response.json()["first_name"] == "admin"
    assert response.json()["last_name"] == "admin"
    assert response.json()["is_active"] is True
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "123"


def test_change_password_success(user_admin):
    response = client.put(
        "/user/password/1", json={"password": "admin", "new_password": "admin123"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(user_admin):
    response = client.put(
        "/user/password/1",
        json={"password": "wrong_password", "new_password": "admin123"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The password informed does not match with the current password"
    }


def test_change_phone_number_success(user_admin):
    response = client.patch("/auth/phonenumber/1", json={
        "phone_number": "123"
    })

    assert response.status_code == status.HTTP_200_OK
