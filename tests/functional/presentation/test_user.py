from uuid import uuid4

from fastapi import FastAPI
from httpx import Response

from src.infra.security.base import BasePasswordHasher


async def test_user__create__ok(app: FastAPI, test_client):
    # arrange
    url = app.url_path_for('create_user')
    body = {'username': 'username 1', 'password': 'Password123!', 'email': 'test@mail.ru'}

    # act
    response: Response = await test_client.post(url=url, json=body)

    # assert
    assert response.status_code == 201
    assert response.json()['token']


async def test_user__create__400(app: FastAPI, test_client):
    # arrange
    url = app.url_path_for('create_user')
    body = {'username': 'username 1', 'password': 'password', 'email': 'test@mail.ru'}

    # act
    response: Response = await test_client.post(url=url, json=body)

    # assert
    assert response.status_code == 400


async def test_user__auth__ok(app, test_client, container, insert_user):
    # arrange
    hasher: BasePasswordHasher = container.resolve(BasePasswordHasher)
    password = 'Password123!'
    await insert_user(username='username 1', password=hasher.hash_password(password))

    url = app.url_path_for('auth_user')
    body = {'username': 'username 1', 'password': 'Password123!'}

    # act
    response = await test_client.post(url, json=body)

    # assert
    assert response.status_code == 200
    assert 'token' in response.json()


async def test_user__auth__401(app, test_client):
    # arrange
    url = app.url_path_for('auth_user')
    body = {'username': 'username 1', 'password': 'password'}
    expected_error = {'detail': 'Неверный логин или пароль!'}

    # act
    response: Response = await test_client.post(url=url, json=body)

    # assert
    assert response.status_code == 401
    assert response.json() == expected_error


async def test_user__get_by_id__ok(app: FastAPI, test_client, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)
    url = app.url_path_for('get_user_by_id', user_id=user_id)

    # act
    response = await test_client.get(url)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(user_id)


async def test_user__get_by_id__404(app: FastAPI, test_client):
    # arrange
    url = app.url_path_for('get_user_by_id', user_id=uuid4())

    # act
    response = await test_client.get(url)

    # assert
    assert response.status_code == 404
