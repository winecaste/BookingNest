import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("name@example.com", 'something', 201),
    ("nick23@egmail.com", '12w4ds12x', 201),
    ("just_string", 'xnDEdj242a', 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(url="/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", 'test', 200),
    ("artem@example.com", 'artem', 200),
    ("fake@fake.com", 'xnDEdj242a', 401),
    ("nick23@egmail.com", '12w4ds12x', 200)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(url="/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
