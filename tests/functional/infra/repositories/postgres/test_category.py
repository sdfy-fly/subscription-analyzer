from uuid import uuid4

import pytest

from src.domain.entity.category import Category
from src.domain.repositories.category import BaseCategoryRepository
from src.domain.values.category import Name


@pytest.fixture(name='category_repo')
async def get_category_repo(container, pg_session):
    repo: BaseCategoryRepository = container.resolve(BaseCategoryRepository, session=pg_session)
    yield repo


async def test_category__create(category_repo, pg_session, pg, insert_user):
    # arrange
    user_id = uuid4()
    category = Category(name=Name('category 1'), user_id=user_id)
    await insert_user(user_id=user_id)

    # act
    await category_repo.create(category)
    await pg_session.commit()

    # assert
    categories_in_db = await pg.fetch('SELECT * FROM categories')
    assert len(categories_in_db) == 1
    category_in_db = categories_in_db[0]

    assert category_in_db['id'] == category.id
    assert category_in_db['name'] == category.name.value
    assert category_in_db['user_id'] == category.user_id
    assert category_in_db['created_at'] == category.created_at
    assert category_in_db['updated_at'] == category.updated_at


@pytest.mark.parametrize(
    'new_category, existing_category, expected_result',
    [
        ('category 1', 'category 1', True),
        ('category 2', 'category 1', False),
    ],
)
async def test_category__is_category_exists(
    category_repo, pg_session, pg, insert_user, new_category, existing_category, expected_result
):
    # arrange
    user_id = uuid4()
    old_category = Category(name=Name(existing_category), user_id=user_id)
    category = Category(name=Name(new_category), user_id=user_id)
    await insert_user(user_id=user_id)

    # act
    await category_repo.create(old_category)
    await pg_session.commit()
    result = await category_repo.is_category_exists(category)

    # assert
    assert result is expected_result


async def test_category__get_by_id__ok(category_repo, pg_session, pg, insert_user):
    # arrange
    user_id = uuid4()
    category = Category(name=Name('category 1'), user_id=user_id)
    await insert_user(user_id=user_id)
    await category_repo.create(category)
    await pg_session.commit()

    # act
    category_from_repo = await category_repo.get_by_id(category.id)

    # assert
    assert category_from_repo == category


async def test_category__get_by_id__not_found(category_repo):
    # act
    category = await category_repo.get_by_id(uuid4())

    # assert
    assert category is None


async def test_category__get_user_categories(category_repo, pg_session, pg, insert_user):
    # arrange
    user_id = uuid4()
    category1 = Category(name=Name('category 1'), user_id=user_id)
    category2 = Category(name=Name('category 2'), user_id=user_id)
    await insert_user(user_id=user_id)
    await category_repo.create(category1)
    await category_repo.create(category2)
    await pg_session.commit()

    # act
    user_categories = await category_repo.get_user_categories(user_id)

    # assert
    assert len(user_categories) == 2
    assert user_categories == [category1, category2]


async def test_category__get_user_categories__empty(category_repo, pg_session, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)

    # act
    user_categories = await category_repo.get_user_categories(user_id)

    # assert
    assert user_categories == []


async def test_category__update(category_repo, pg_session, pg, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)

    category = Category(name=Name('Original Category'), user_id=user_id)
    await category_repo.create(category)
    await pg_session.commit()

    # act
    category.name = Name('Updated Category')
    updated_category = await category_repo.update(category)
    await pg_session.commit()

    # assert
    # проверяем ответ репозитория
    assert updated_category is not None
    assert updated_category.id == category.id
    assert updated_category.name.value == 'Updated Category'
    assert updated_category.user_id == category.user_id
    assert updated_category.created_at == category.created_at
    assert updated_category.updated_at > category.updated_at

    # проверяем обновление в базе
    category_in_db = await pg.fetchrow('SELECT * FROM categories WHERE id = $1', category.id)
    assert category_in_db is not None
    assert category_in_db['id'] == category.id
    assert category_in_db['name'] == 'Updated Category'
    assert category_in_db['user_id'] == category.user_id
    assert category_in_db['created_at'] == category.created_at
    assert category_in_db['updated_at'] == updated_category.updated_at


async def test_category__remove(category_repo, insert_category, insert_user, pg, pg_session):
    # arrange
    category_id = uuid4()
    user_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id)

    # act
    category_before = await pg.fetch('SELECT * FROM categories')
    await category_repo.remove(category_id)
    await pg_session.commit()
    category_after = await pg.fetch('SELECT * FROM categories')

    # assert
    assert len(category_before) == 1
    assert len(category_after) == 0


async def test_category__remove__category_does_not_exists(category_repo, insert_category, insert_user, pg, pg_session):
    # arrange
    category_id = uuid4()
    user_id = uuid4()
    random_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id)

    # act
    category_before = await pg.fetch('SELECT * FROM categories')
    await category_repo.remove(random_id)
    await pg_session.commit()
    category_after = await pg.fetch('SELECT * FROM categories')

    # assert
    assert len(category_before) == 1
    assert len(category_after) == 1
