from uuid import uuid4

import pytest

from src.domain.entity.category import Category
from src.domain.exceptions.category import CategoryNameRequired, CategoryNameTooLong
from src.domain.values.category import Name


def get_category(name: str):
    return Category(name=Name(name), user_id=uuid4())


@pytest.mark.parametrize(
    'name, exception, message',
    [
        ('', CategoryNameRequired, 'Категории необходимо задать название!'),
        (' ', CategoryNameRequired, 'Категории необходимо задать название!'),
        ('x' * 101, CategoryNameTooLong, f'Слишком длинное название для категории: {"x" * 101}'),
    ],
)
def test_category__invalid_name(name, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_category(name=name)

    # assert
    assert str(e.value.message) == message


def test_category__ok():
    # arrange
    name = Name(value='some name')
    user_id = uuid4()

    # act
    category = Category(name=name, user_id=user_id)

    # assert
    assert category.name.value == 'some name'
    assert category.user_id == user_id
