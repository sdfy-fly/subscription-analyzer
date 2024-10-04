import pytest

from src.domain.entity.user import User
from src.domain.exceptions.user import (
    EmailRequiredException,
    InvalidEmailException,
    PasswordMissingDigitException,
    PasswordMissingSpecialCharacterException,
    PasswordMissingUppercaseException,
    PasswordRequiredException,
    PasswordTooLongException,
    PasswordTooShortException,
    UsernameRequiredException,
    UsernameTooLongException,
    UsernameTooShortException,
)
from src.domain.values.user import Email, Password, Username


def get_user(username: str = 'test123', password: str = 'Qwerty!123', email: str | None = None):
    email = Email(value=email) if email is not None else None
    return User(username=Username(value=username), password=Password(value=password), email=email)


@pytest.mark.parametrize(
    'username, exception, message',
    [
        ('', UsernameRequiredException, 'Необходимо указать username!'),
        (' ', UsernameRequiredException, 'Необходимо указать username!'),
        ('ab', UsernameTooShortException, 'Длина username должна быть как минимум 4 символа!'),
        ('123', UsernameTooShortException, 'Длина username должна быть как минимум 4 символа!'),
        ('123', UsernameTooShortException, 'Длина username должна быть как минимум 4 символа!'),
        ('x' * 101, UsernameTooLongException, f'Слишком длинный username: {"x" * 101}'),
    ],
)
def test_user__invalid_username(username, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_user(username=username)

    # assert
    assert str(e.value.message()) == message


@pytest.mark.parametrize(
    'password, exception, message',
    [
        ('', PasswordRequiredException, 'Необходимо указать пароль!'),
        (' ', PasswordRequiredException, 'Необходимо указать пароль!'),
        ('test', PasswordTooShortException, 'Пароль должен содержать как минимум 8 символов!'),
        ('test123', PasswordTooShortException, 'Пароль должен содержать как минимум 8 символов!'),
        ('test1234', PasswordMissingUppercaseException, 'Пароль должен содержать хотя бы 1 заглавный символ.'),
        ('Test1234', PasswordMissingSpecialCharacterException, 'Пароль должен содержать хотя бы один спец символ.'),
        ('Test!qwerty', PasswordMissingDigitException, 'Пароль должен содержать хотя бы одну цифру.'),
        ('x' * 101, PasswordTooLongException, 'Пароль не должен превышать 100 символов!'),
    ],
)
def test_user__invalid_password(password, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_user(password=password)

    # act
    assert str(e.value.message()) == message


@pytest.mark.parametrize(
    'email, exception, message',
    [
        ('', EmailRequiredException, 'Нельзя указать пустой email!'),
        (' ', EmailRequiredException, 'Нельзя указать пустой email!'),
        ('invalidemail', InvalidEmailException, 'Некорректный email: invalidemail'),
        ('invalid@', InvalidEmailException, 'Некорректный email: invalid@'),
        ('invalid@domain', InvalidEmailException, 'Некорректный email: invalid@domain'),
        ('invalid@domain.', InvalidEmailException, 'Некорректный email: invalid@domain.'),
        ('invalid@domain.q', InvalidEmailException, 'Некорректный email: invalid@domain.q'),
    ],
)
def test_user__invalid_email(email, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_user(email=email)

    # assert
    assert str(e.value.message()) == message


def test_user__ok():
    # arrange
    username = Username('test user 1')
    password = Password('UserPassword1!')
    email = Email('user.email@test.com')

    # act
    user = User(username=username, password=password, email=email)

    # assert
    assert user.username.value == 'test user 1'
    assert user.password.value == 'UserPassword1!'
    assert user.email.value == 'user.email@test.com'
