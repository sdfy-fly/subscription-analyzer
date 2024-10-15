from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass
class UsernameRequiredException(ApplicationException):
    def message(self):
        return 'Необходимо указать username!'


@dataclass
class UsernameTooShortException(ApplicationException):
    def message(self):
        return 'Длина username должна быть как минимум 4 символа!'


@dataclass
class UsernameTooLongException(ApplicationException):
    username: str

    def message(self):
        return f'Слишком длинный username: {self.username}'


@dataclass
class PasswordRequiredException(ApplicationException):
    def message(self):
        return 'Необходимо указать пароль!'


@dataclass
class PasswordTooShortException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать как минимум 8 символов!'


@dataclass
class PasswordTooLongException(ApplicationException):
    def message(self):
        return 'Пароль не должен превышать 100 символов!'


@dataclass
class PasswordMissingUppercaseException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы 1 заглавный символ.'


@dataclass
class PasswordMissingSpecialCharacterException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы один спец символ.'


@dataclass
class PasswordMissingDigitException(ApplicationException):
    def message(self):
        return 'Пароль должен содержать хотя бы одну цифру.'


@dataclass
class EmailRequiredException(ApplicationException):
    def message(self):
        return 'Нельзя указать пустой email!'


@dataclass
class InvalidEmailException(ApplicationException):
    email: str

    def message(self):
        return f'Некорректный email: {self.email}'
