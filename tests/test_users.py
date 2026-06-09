# Тесты управления профилем пользователя


async def test_get_me(async_client, auth_headers):
    # Успешное получение профиля текущего пользователя
    response = await async_client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"
    assert "id" in response.json()


async def test_get_me_unauthorized(async_client):
    # Запрос без токена возвращает 401
    response = await async_client.get("/users/me")
    assert response.status_code == 401


async def test_update_user_email(async_client, auth_headers):
    # Успешное обновление email пользователя
    response = await async_client.patch("/users/me",
                                        json={"email": "updated@test.com"},
                                        headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "updated@test.com"


async def test_update_user_unauthorized(async_client):
    # Обновление профиля без токена возвращает 401
    response = await async_client.patch("/users/me", json={"email": "updated@test.com"})
    assert response.status_code == 401
