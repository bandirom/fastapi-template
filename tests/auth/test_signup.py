from typing import TYPE_CHECKING

import pytest

from db.models import User

if TYPE_CHECKING:
    from httpx import AsyncClient
    from sqlalchemy.ext.asyncio import AsyncSession


SIGN_UP_ENDPOINT = "/api/v1/auth/sign-up"


@pytest.mark.asyncio
async def test_successful_signup(client: "AsyncClient", db_session: "AsyncSession"):
    payload = {
        "email": "valid@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Str0ng!Pass",
        "password_confirm": "Str0ng!Pass",
    }

    response = await client.post(SIGN_UP_ENDPOINT, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

    user = await db_session.get(User, data["id"])
    assert user and user.email == payload["email"]


@pytest.mark.asyncio
async def test_duplicate_email_signup(client: "AsyncClient", user: "User"):

    payload = {
        "email": "margo.robbie@email.com",
        "first_name": "Another",
        "last_name": "User",
        "password": "Str0ng!Pass",
        "password_confirm": "Str0ng!Pass",
    }

    response = await client.post(SIGN_UP_ENDPOINT, json=payload)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert {"email": "User with this email already exist"} in detail


@pytest.mark.asyncio
async def test_passwords_do_not_match(client: "AsyncClient"):
    payload = {
        "email": "mismatch@example.com",
        "first_name": "Mismatch",
        "last_name": "User",
        "password": "Str0ng!Pass",
        "password_confirm": "Wrong!Pass",
    }

    response = await client.post(SIGN_UP_ENDPOINT, json=payload)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert any("password_confirm" in e and "Passwords do not match" in e["password_confirm"] for e in detail)
