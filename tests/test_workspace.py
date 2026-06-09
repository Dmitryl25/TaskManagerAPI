import pytest
from uuid import uuid4

# Тесты управления workspace


async def test_create_workspace(async_client, auth_headers):
    # Успешное создание workspace
    response = await async_client.post("/workspace",
                                       json={"name": "My WS", "description": "desc"},
                                       headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "My WS"


async def test_get_workspaces_empty(async_client, auth_headers):
    # Пустой список workspace для нового пользователя
    response = await async_client.get("/workspace", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_workspaces(async_client, auth_headers, workspace_id):
    # Список workspace содержит созданный workspace
    response = await async_client.get("/workspace", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == workspace_id


async def test_get_workspace_by_id(async_client, auth_headers, workspace_id):
    # Успешное получение workspace по id
    response = await async_client.get(f"/workspace/{workspace_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == workspace_id


async def test_get_workspace_not_found(async_client, auth_headers):
    # Несуществующий workspace возвращает 404
    response = await async_client.get(f"/workspace/{uuid4()}", headers=auth_headers)
    assert response.status_code == 404


async def test_get_workspace_not_member(async_client, auth_headers, second_auth_headers, workspace_id):
    # Пользователь не-член workspace получает 403
    response = await async_client.get(f"/workspace/{workspace_id}", headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_workspace(async_client, auth_headers, workspace_id):
    # Успешное обновление workspace
    response = await async_client.patch(f"/workspace/{workspace_id}",
                                        json={"name": "Updated WS"},
                                        headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated WS"


async def test_delete_workspace(async_client, auth_headers, workspace_id):
    # Владелец может удалить workspace
    response = await async_client.delete(f"/workspace/{workspace_id}", headers=auth_headers)
    assert response.status_code == 204


async def test_delete_workspace_not_owner(async_client, auth_headers, second_auth_headers,
                                          second_user_id, workspace_id):
    # Обычный участник не может удалить workspace
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)
    response = await async_client.delete(f"/workspace/{workspace_id}", headers=second_auth_headers)
    assert response.status_code == 403


async def test_get_workspace_members(async_client, auth_headers, workspace_id):
    # Список участников содержит создателя workspace
    response = await async_client.get(f"/workspace/{workspace_id}/members", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_add_member(async_client, auth_headers, second_user_id, workspace_id):
    # Владелец может добавить нового участника
    response = await async_client.post(f"/workspace/{workspace_id}/members",
                                       json={"user_id": second_user_id, "role": "member"},
                                       headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == second_user_id


async def test_add_member_not_admin(async_client, auth_headers, second_auth_headers,
                                    second_user_id, workspace_id):
    # Участник без прав admin/owner не может добавить нового участника
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)

    await async_client.post("/auth/register", json={"email": "user3@test.com", "password": "pass1234"})
    login_resp = await async_client.post("/auth/login", json={"email": "user3@test.com", "password": "pass1234"})
    user3_id_resp = await async_client.get("/users/me",
                                           headers={"Authorization": f"Bearer {login_resp.json()['access_token']}"})
    user3_id = user3_id_resp.json()["id"]

    response = await async_client.post(f"/workspace/{workspace_id}/members",
                                       json={"user_id": user3_id, "role": "member"},
                                       headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_member_role(async_client, auth_headers, second_user_id, workspace_id):
    # Владелец может изменить роль участника
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)
    response = await async_client.patch(f"/workspace/{workspace_id}/members/{second_user_id}",
                                        json={"role": "admin"},
                                        headers=auth_headers)
    assert response.status_code == 200


async def test_remove_member(async_client, auth_headers, second_user_id, workspace_id):
    # Владелец может удалить участника
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)
    response = await async_client.delete(f"/workspace/{workspace_id}/members/{second_user_id}",
                                         headers=auth_headers)
    assert response.status_code == 204
