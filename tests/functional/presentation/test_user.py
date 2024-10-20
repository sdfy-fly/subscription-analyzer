from uuid import uuid4

from fastapi import FastAPI, status
from httpx import Response


async def test_user__create__ok(app: FastAPI, test_client):
    url = app.url_path_for('create_user')
    body = {
        'username': 'username 1',
        'password': 'Password123!',
        'email': 'test@mail.ru'
    }
    response: Response = await test_client.post(url=url, json=body)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['token']


async def test_user__create__400(app: FastAPI, test_client):
    url = app.url_path_for('create_user')
    body = {
        'username': 'username 1',
        'password': 'password',
        'email': 'test@mail.ru'
    }
    response: Response = await test_client.post(url=url, json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_user__get_by_id__ok(app: FastAPI, test_client, insert_user):
    user_id = uuid4()
    await insert_user(user_id=user_id)
    url = app.url_path_for('get_user_by_id', user_id=user_id)

    response = await test_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == str(user_id)


async def test_user__get_by_id__404(app: FastAPI, test_client):
    url = app.url_path_for('get_user_by_id', user_id=uuid4())
    response = await test_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
