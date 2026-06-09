from uuid import uuid4

# Тесты управления комментариями


async def test_create_comment(async_client, auth_headers, task_id):
    # Успешное создание комментария к задаче
    response = await async_client.post(f"/tasks/{task_id}/comments",
                                       json={"content": "Great task!"},
                                       headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Great task!"
    assert response.json()["task_id"] == task_id


async def test_create_comment_not_member(async_client, second_auth_headers, task_id):
    # Не-член workspace не может оставить комментарий
    response = await async_client.post(f"/tasks/{task_id}/comments",
                                       json={"content": "comment"},
                                       headers=second_auth_headers)
    assert response.status_code == 403


async def test_create_comment_task_not_found(async_client, auth_headers):
    # Комментарий к несуществующей задаче возвращает 404
    response = await async_client.post(f"/tasks/{uuid4()}/comments",
                                       json={"content": "comment"},
                                       headers=auth_headers)
    assert response.status_code == 404


async def test_get_task_comments(async_client, auth_headers, task_id, comment_id):
    # Список комментариев задачи содержит созданный комментарий
    response = await async_client.get(f"/tasks/{task_id}/comments", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == comment_id


async def test_get_task_comments_empty(async_client, auth_headers, task_id):
    # Пустой список комментариев для задачи без комментариев
    response = await async_client.get(f"/tasks/{task_id}/comments", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_task_comments_not_member(async_client, second_auth_headers, task_id):
    # Не-член workspace не может получить комментарии
    response = await async_client.get(f"/tasks/{task_id}/comments", headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_comment(async_client, auth_headers, comment_id):
    # Автор может обновить свой комментарий
    response = await async_client.patch(f"/comments/{comment_id}",
                                        json={"content": "Updated comment"},
                                        headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated comment"


async def test_update_comment_not_author(async_client, auth_headers, second_auth_headers,
                                         second_user_id, workspace_id, task_id, comment_id):
    # Не-автор не может обновить чужой комментарий
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)
    response = await async_client.patch(f"/comments/{comment_id}",
                                        json={"content": "Hacked!"},
                                        headers=second_auth_headers)
    assert response.status_code == 403


async def test_update_comment_not_found(async_client, auth_headers):
    # Обновление несуществующего комментария возвращает 404
    response = await async_client.patch(f"/comments/{uuid4()}",
                                        json={"content": "comment"},
                                        headers=auth_headers)
    assert response.status_code == 404


async def test_delete_comment(async_client, auth_headers, comment_id):
    # Автор может удалить свой комментарий
    response = await async_client.delete(f"/comments/{comment_id}", headers=auth_headers)
    assert response.status_code == 204


async def test_delete_comment_not_author(async_client, auth_headers, second_auth_headers,
                                         second_user_id, workspace_id, task_id, comment_id):
    # Не-автор не может удалить чужой комментарий
    await async_client.post(f"/workspace/{workspace_id}/members",
                            json={"user_id": second_user_id, "role": "member"},
                            headers=auth_headers)
    response = await async_client.delete(f"/comments/{comment_id}", headers=second_auth_headers)
    assert response.status_code == 403


async def test_delete_comment_not_found(async_client, auth_headers):
    # Удаление несуществующего комментария возвращает 404
    response = await async_client.delete(f"/comments/{uuid4()}", headers=auth_headers)
    assert response.status_code == 404
