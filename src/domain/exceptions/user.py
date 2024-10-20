from dataclasses import dataclass

from src.domain.exceptions.base import DomainException


@dataclass
class UsernameRequiredException(DomainException):
    @property
    def message(self):
        return 'Необходимо указать username!'


@dataclass
class UsernameTooShortException(DomainException):
    @property
    def message(self):
        return 'Длина username должна быть как минимум 4 символа!'


@dataclass
class UsernameTooLongException(DomainException):
    username: str

    @property
    def message(self):
        return f'Слишком длинный username: {self.username}'


@dataclass
class PasswordRequiredException(DomainException):
    @property
    def message(self):
        return 'Необходимо указать пароль!'


@dataclass
class PasswordTooShortException(DomainException):
    @property
    def message(self):
        return 'Пароль должен содержать как минимум 8 символов!'


@dataclass
class PasswordTooLongException(DomainException):
    @property
    def message(self):
        return 'Пароль не должен превышать 100 символов!'


@dataclass
class PasswordMissingUppercaseException(DomainException):
    @property
    def message(self):
        return 'Пароль должен содержать хотя бы 1 заглавный символ.'


@dataclass
class PasswordMissingSpecialCharacterException(DomainException):
    @property
    def message(self):
        return 'Пароль должен содержать хотя бы один спец символ.'


@dataclass
class PasswordMissingDigitException(DomainException):
    @property
    def message(self):
        return 'Пароль должен содержать хотя бы одну цифру.'


@dataclass
class EmailRequiredException(DomainException):
    @property
    def message(self):
        return 'Нельзя указать пустой email!'


@dataclass
class InvalidEmailException(DomainException):
    email: str

    @property
    def message(self):
        return f'Некорректный email: {self.email}'
