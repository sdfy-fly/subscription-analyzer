import pytest

from src.domain.entity.category import Category
from src.domain.exceptions.category import CategoryNameRequired, CategoryNameTooLong
from src.domain.values.category import Name


@pytest.mark.parametrize('name', ['', ' '])
def test_subscription__empty_name(name):
    with pytest.raises(CategoryNameRequired) as e:
        Category(name=Name(value=name))
        assert str(e) == 'Категории необходимо задать название!'


def test_category__name_too_long():
    name = 'name' * 100
    with pytest.raises(CategoryNameTooLong) as e:
        Category(name=Name(value=name))
        assert str(e) == f'Слишком длинное название для категории: {name}'
