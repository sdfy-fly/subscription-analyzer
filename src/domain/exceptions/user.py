from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True)
class UsernameRequiredException(ApplicationException):
    def message(self):
        return 'Необходимо указать username!'


@dataclass(frozen=True)
class UsernameTooShortException(ApplicationException):
    def message(self):
        return 'Длина username должна быть как минимум 4 символа!'


@dataclass(frozen=True)
class UsernameTooLongException(ApplicationException):
    username: str

    def message(self):
        return f'Слишком длинный username: {self.username}'


@dataclass(frozen=True)
class PasswordRequiredException(ApplicationException):
    def message(self):
        return 'Необходимо указать пароль!'


@dataclass(frozen=True)
class PasswordTooShortException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать как минимум 8 символов!'


@dataclass(frozen=True)
class PasswordTooLongException(ApplicationException):
    def message(self):
        return 'Пароль не должен превышать 100 символов!'


@dataclass(frozen=True)
class PasswordMissingUppercaseException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы 1 заглавный символ.'


@dataclass(frozen=True)
class PasswordMissingSpecialCharacterException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы один спец символ.'


@dataclass(frozen=True)
class PasswordMissingDigitException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы одну цифру.'


@dataclass(frozen=True)
class EmailRequiredException(ApplicationException):
    def message(self):
        return 'Нельзя указать пустой email!'


@dataclass(frozen=True)
class InvalidEmailException(ApplicationException):
    email: str

    def message(self):
        return f'Некорректный email: {self.email}'
