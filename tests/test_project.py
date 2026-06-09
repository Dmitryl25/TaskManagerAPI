from uuid import uuid4

# Тесты управления проектами


async def test_create_project(async_client, auth_headers, workspace_id):
    # Успешное создание проекта в workspace
    response = await async_client.post(f"/workspaces/{workspace_id}/projects",
                                       json={"name": "My Project", "description": "desc", "key": "MP"},
                                       headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "My Project"
    assert response.json()["key"] == "MP"


async def test_get_workspace_projects(async_client, auth_headers, workspace_id, project_id):
    # Список проектов workspace содержит созданный проект
    response = await async_client.get(f"/workspaces/{workspace_id}/projects", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == project_id


async def test_get_workspace_projects_empty(async_client, auth_headers, workspace_id):
    # Пустой список проектов для нового workspace
    response = await async_client.get(f"/workspaces/{workspace_id}/projects", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_workspace_projects_not_member(async_client, second_auth_headers, workspace_id):
    # Не-член workspace не может видеть проекты
    response = await async_client.get(f"/workspaces/{workspace_id}/projects",
                                      headers=second_auth_headers)
    assert response.status_code == 403


async def test_get_project_by_id(async_client, auth_headers, project_id):
    # Успешное получение проекта по id
    response = await async_client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == project_id


async def test_get_project_not_found(async_client, auth_headers):
    # Несуществующий проект возвращает 404
    response = await async_client.get(f"/projects/{uuid4()}", headers=auth_headers)
    assert response.status_code == 404


async def test_get_project_not_member(async_client, second_auth_headers, project_id):
    # Не-член workspace не может получить проект
    response = await async_client.get(f"/projects/{project_id}", headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_project(async_client, auth_headers, project_id):
    # Успешное обновление проекта
    response = await async_client.patch(f"/projects/{project_id}",
                                        json={"name": "Updated Project", "status": "active"},
                                        headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"


async def test_delete_project(async_client, auth_headers, project_id):
    # Успешное удаление проекта
    response = await async_client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204


async def test_delete_project_not_member(async_client, second_auth_headers, project_id):
    # Не-член workspace не может удалить проект
    response = await async_client.delete(f"/projects/{project_id}", headers=second_auth_headers)
    assert response.status_code == 403
