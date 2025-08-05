from typing import TYPE_CHECKING

import pytest

from api.errors.codes import ErrorCode

if TYPE_CHECKING:
    from httpx import AsyncClient

    from db.models import User

LOGIN_ENDPOINT = "/api/v1/auth/sign-in"


@pytest.mark.asyncio
async def test_successful_login(client: "AsyncClient", user: "User"):
    response = await client.post(
        LOGIN_ENDPOINT,
        data={"username": user.email, "password": "tester26"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, response.json()
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_user_not_found(client: "AsyncClient"):
    response = await client.post(
        LOGIN_ENDPOINT,
        data={"username": "notfound@example.com", "password": "whatever"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.WRONG_CREDENTIALS.code


@pytest.mark.asyncio
async def test_inactive_user(client: "AsyncClient", user, db_session):
    user.is_active = False
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        LOGIN_ENDPOINT,
        data={"username": user.email, "password": "tester26"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.NOT_ACTIVE.code
