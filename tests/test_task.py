from uuid import uuid4

# Тесты управления задачами


async def test_create_task(async_client, auth_headers, project_id):
    # Успешное создание задачи в проекте
    response = await async_client.post(f"/projects/{project_id}/tasks",
                                       json={"title": "My Task", "description": "desc"},
                                       headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My Task"
    assert response.json()["status"] == "TODO"
    assert response.json()["priority"] == "MEDIUM"


async def test_create_task_not_member(async_client, second_auth_headers, project_id):
    # Не-член workspace не может создать задачу
    response = await async_client.post(f"/projects/{project_id}/tasks",
                                       json={"title": "My Task"},
                                       headers=second_auth_headers)
    assert response.status_code == 403


async def test_create_task_project_not_found(async_client, auth_headers):
    # Создание задачи в несуществующем проекте возвращает 404
    response = await async_client.post(f"/projects/{uuid4()}/tasks",
                                       json={"title": "My Task"},
                                       headers=auth_headers)
    assert response.status_code == 404


async def test_get_project_tasks(async_client, auth_headers, project_id, task_id):
    # Список задач проекта содержит созданную задачу
    response = await async_client.get(f"/projects/{project_id}/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id


async def test_get_project_tasks_empty(async_client, auth_headers, project_id):
    # Пустой список задач для нового проекта
    response = await async_client.get(f"/projects/{project_id}/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_project_tasks_filter_by_status(async_client, auth_headers, project_id, task_id):
    # Фильтрация задач по статусу возвращает совпадающие задачи
    response = await async_client.get(f"/projects/{project_id}/tasks?status=TODO",
                                      headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await async_client.get(f"/projects/{project_id}/tasks?status=DONE",
                                      headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_project_tasks_filter_by_priority(async_client, auth_headers, project_id, task_id):
    # Фильтрация задач по приоритету возвращает совпадающие задачи
    response = await async_client.get(f"/projects/{project_id}/tasks?priority=MEDIUM",
                                      headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await async_client.get(f"/projects/{project_id}/tasks?priority=HIGH",
                                      headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_task_by_id(async_client, auth_headers, task_id):
    # Успешное получение задачи по id
    response = await async_client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id


async def test_get_task_not_found(async_client, auth_headers):
    # Несуществующая задача возвращает 404
    response = await async_client.get(f"/tasks/{uuid4()}", headers=auth_headers)
    assert response.status_code == 404


async def test_get_task_not_member(async_client, second_auth_headers, task_id):
    # Не-член workspace не может получить задачу
    response = await async_client.get(f"/tasks/{task_id}", headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_task(async_client, auth_headers, task_id):
    # Успешное обновление задачи
    response = await async_client.patch(f"/tasks/{task_id}",
                                        json={"title": "Updated Task", "status": "in_progress"},
                                        headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "in_progress"


async def test_delete_task(async_client, auth_headers, task_id):
    # Успешное удаление задачи
    response = await async_client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204


async def test_delete_task_not_member(async_client, second_auth_headers, task_id):
    # Не-член workspace не может удалить задачу
    response = await async_client.delete(f"/tasks/{task_id}", headers=second_auth_headers)
    assert response.status_code == 403
