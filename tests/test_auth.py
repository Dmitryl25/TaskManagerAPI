async def test_register(async_client):
    response = await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                               "password": "dmdw1234"})
    assert response.status_code == 201
    assert response.json()["email"] == "dima@example.com"

async def test_repeat_register(async_client):
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})

    response = await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                               "password": "dmdw1234"})
    assert response.status_code == 400

async def test_login(async_client):
    await async_client.post("/auth/register", json={"email": "dima@example.com",
                                                    "password": "dmdw1234"})


    response = await async_client.post("/auth/login", json={"email": "dima@example.com",
                                                            "password": "dmdw1234"})
    assert response.status_code == 200
    assert response.json()["access_token"] and response.json()["refresh_token"]