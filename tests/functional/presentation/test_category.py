from uuid import uuid4

from src.domain.helpers import get_utc_now


async def test_category__create__ok(get_auth_header, test_client, app, pg):
    # arrange
    user_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    url = app.url_path_for('create_category')
    body = {'name': 'category 1'}

    # act
    response = await test_client.post(url, json=body, headers=headers)

    # assert
    assert response.status_code == 201
    data = response.json()
    category = await pg.fetchrow('SELECT * from categories')
    assert data['id'] == str(category['id'])
    assert data['name'] == category['name']
    assert category['user_id'] == user_id


async def test_category__create__already_exists(get_auth_header, test_client, app, insert_category):
    # arrange
    user_id = uuid4()
    category_name = 'category 1'
    headers = await get_auth_header(user_id=user_id, create=True)
    url = app.url_path_for('create_category')
    body = {'name': 'category 1'}

    # act
    await insert_category(name=category_name, user_id=user_id)
    response = await test_client.post(url, json=body, headers=headers)

    # assert
    assert response.status_code == 400


async def test_get_category_by_id__ok(get_auth_header, test_client, app, insert_category, mediator):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    await insert_category(category_id=category_id, user_id=user_id, name='Test Category')
    url = app.url_path_for('get_category_by_id', category_id=str(category_id))

    # act
    response = await test_client.get(url, headers=headers)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(category_id)
    assert data['name'] == 'Test Category'


async def test_get_category_by_id__not_found(get_auth_header, test_client, app):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id)
    url = app.url_path_for('get_category_by_id', category_id=str(category_id))

    # act
    response = await test_client.get(url, headers=headers)

    # assert
    assert response.status_code == 404


async def test_get_category_by_id__forbidden(get_auth_header, test_client, app, insert_category, insert_user):
    # arrange
    user_id = uuid4()
    another_user_id = uuid4()
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id)
    await insert_user(user_id=another_user_id)
    await insert_category(category_id=category_id, user_id=another_user_id, name='Forbidden Category')
    url = app.url_path_for('get_category_by_id', category_id=str(category_id))

    # act
    response = await test_client.get(url, headers=headers)

    # assert
    assert response.status_code == 403


async def test_get_user_categories__ok(get_auth_header, test_client, app, insert_category):
    # arrange
    user_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    created_updated_ts = get_utc_now()
    category_1_id = uuid4()
    category_2_id = uuid4()
    await insert_category(
        category_id=category_1_id, user_id=user_id, name='Category 1', created_updated_ts=created_updated_ts
    )
    await insert_category(
        category_id=category_2_id, user_id=user_id, name='Category 2', created_updated_ts=created_updated_ts
    )
    formatted_ts = created_updated_ts.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
    expected_response = [
        {
            'id': str(category_1_id),
            'name': 'Category 1',
            'created_at': formatted_ts,
            'updated_at': formatted_ts,
        },
        {
            'id': str(category_2_id),
            'name': 'Category 2',
            'created_at': formatted_ts,
            'updated_at': formatted_ts,
        },
    ]
    url = app.url_path_for('get_user_categories')

    # act
    response = await test_client.get(url, headers=headers)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data == expected_response


async def test_get_user_categories__empty(get_auth_header, test_client, app):
    # arrange
    headers = await get_auth_header(user_id=uuid4())
    url = app.url_path_for('get_user_categories')

    # act
    response = await test_client.get(url, headers=headers)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data == []


async def test_update_category__ok(get_auth_header, test_client, app, insert_category):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    await insert_category(category_id=category_id, user_id=user_id, name='Old Category')
    url = app.url_path_for('update_category', category_id=category_id)
    body = {'name': 'Updated Category'}

    # act
    response = await test_client.put(url, json=body, headers=headers)

    # assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(category_id)
    assert data['name'] == 'Updated Category'


async def test_update_category__not_found(get_auth_header, test_client, app):
    # arrange
    user_id = uuid4()
    category_id = uuid4()  # Неправильный ID
    headers = await get_auth_header(user_id=user_id)
    url = app.url_path_for('update_category', category_id=category_id)
    body = {'name': 'Updated Category'}

    # act
    response = await test_client.put(url, json=body, headers=headers)

    # assert
    assert response.status_code == 404


async def test_update_category__forbidden(get_auth_header, test_client, app, insert_category, insert_user):
    # arrange
    user_id = uuid4()
    other_user_id = uuid4()  # ID другого пользователя
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id)
    await insert_user(user_id=user_id)
    await insert_user(user_id=other_user_id)
    await insert_category(category_id=category_id, user_id=other_user_id, name='Old Category')
    url = app.url_path_for('update_category', category_id=category_id)
    body = {'name': 'Updated Category'}

    # act
    response = await test_client.put(url, json=body, headers=headers)

    # assert
    assert response.status_code == 403


async def test_update_category__category_already_exists(get_auth_header, test_client, app, insert_category):
    # arrange
    user_id = uuid4()
    category_1_id = uuid4()
    category_2_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    await insert_category(category_id=category_1_id, user_id=user_id, name='Category 1')
    await insert_category(category_id=category_2_id, user_id=user_id, name='Category 2')
    url = app.url_path_for('update_category', category_id=category_2_id)
    body = {'name': 'Category 1'}

    # act
    response = await test_client.put(url, json=body, headers=headers)

    # assert
    assert response.status_code == 400
    data = response.json()

    assert data['detail'] == 'Такая категория уже существует!'


async def test_delete_category__ok(get_auth_header, test_client, app, insert_category):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    await insert_category(category_id=category_id, user_id=user_id, name='Category to delete')
    url = app.url_path_for('delete_category', category_id=category_id)

    # act
    response = await test_client.delete(url, headers=headers)

    # assert
    assert response.status_code == 204


async def test_delete_category__not_found(get_auth_header, test_client, app):
    # arrange
    user_id = uuid4()
    category_id = uuid4()  # Несуществующий ID
    headers = await get_auth_header(user_id=user_id)
    url = app.url_path_for('delete_category', category_id=category_id)

    # act
    response = await test_client.delete(url, headers=headers)

    # assert
    assert response.status_code == 404


async def test_delete_category__forbidden(get_auth_header, test_client, app, insert_category, insert_user):
    # arrange
    user_id = uuid4()
    other_user_id = uuid4()  # ID другого пользователя
    category_id = uuid4()
    headers = await get_auth_header(user_id=user_id, create=True)
    await insert_user(user_id=other_user_id)
    await insert_category(category_id=category_id, user_id=other_user_id, name='Category to delete')
    url = app.url_path_for('delete_category', category_id=category_id)

    # act
    response = await test_client.delete(url, headers=headers)

    # assert
    assert response.status_code == 403
