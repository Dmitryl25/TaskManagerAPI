# Тесты авторизации и аутентификации


async def test_register(async_client):
    # Успешная регистрация нового пользователя
    response = await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                               "password": "dmdw1234"})
    assert response.status_code == 201
    assert response.json()["email"] == "dima@example.com"


async def test_repeat_register(async_client):
    # Повторная регистрация с тем же email возвращает 400
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    response = await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                               "password": "dmdw1234"})
    assert response.status_code == 400


async def test_login(async_client):
    # Успешный вход возвращает access и refresh токены
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    response = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                            "password": "dmdw1234"})
    assert response.status_code == 200
    assert response.json()["access_token"] and response.json()["refresh_token"]


async def test_login_wrong_password(async_client):
    # Неверный пароль возвращает 401
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    response = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                            "password": "wrongpass"})
    assert response.status_code == 401


async def test_login_nonexistent_user(async_client):
    # Вход несуществующего пользователя возвращает 401
    response = await async_client.post("/auth/login", json={"email": "nobody@example.com",
                                                            "password": "dmdw1234"})
    assert response.status_code == 401


async def test_refresh_token(async_client):
    # Обновление токена возвращает новую пару токенов
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    login_resp = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                              "password": "dmdw1234"})
    refresh_token = login_resp.json()["refresh_token"]

    response = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json()["access_token"] and response.json()["refresh_token"]


async def test_refresh_token_invalid(async_client):
    # Невалидный refresh-токен возвращает 401
    response = await async_client.post("/auth/refresh", json={"refresh_token": "invalid.token.here"})
    assert response.status_code == 401



async def test_logout(async_client):
    # Успешный выход инвалидирует refresh-токен
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    login_resp = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                              "password": "dmdw1234"})
    refresh_token = login_resp.json()["refresh_token"]

    response = await async_client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert response.status_code == 204


async def test_logout_then_refresh_fails(async_client):
    # После logout использование refresh-токена возвращает 401
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})
    login_resp = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                              "password": "dmdw1234"})
    refresh_token = login_resp.json()["refresh_token"]

    await async_client.post("/auth/logout", json={"refresh_token": refresh_token})
    response = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 401
