from fastapi import status, HTTPException
from app.config.models import Todos
from .utils import client, TestingSessionLocal, user_admin
from app.routers.auth import (
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    get_current_user,
)
from jose import jwt
from datetime import timedelta
import pytest


def test_authenticate_user(user_admin):

    db = TestingSessionLocal()

    user = authenticate_user(user_admin.username, "admin", db)

    assert user.username == user_admin.username

    non_existent_user = authenticate_user("wrong", "admin", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(user_admin.username, "wrong", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():

    encode = {"sub": "admin", "id": 1, "role": "admin"}

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)

    assert user == {"username": "admin", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate user."
