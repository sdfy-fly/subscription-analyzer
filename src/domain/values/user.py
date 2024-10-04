import re
from dataclasses import dataclass

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
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Username(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise UsernameRequiredException

        if len(self.value) < 4:
            raise UsernameTooShortException

        if len(self.value) > 100:
            raise UsernameTooLongException(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise PasswordRequiredException

        if len(self.value) < 8:
            raise PasswordTooShortException

        if len(self.value) > 100:
            raise PasswordTooLongException

        if not re.search(r'[А-ЯA-Z]', self.value):
            raise PasswordMissingUppercaseException

        if not re.search(r'[!@#$%^&*\-_+]', self.value):
            raise PasswordMissingSpecialCharacterException

        if not re.search(r'\d', self.value):
            raise PasswordMissingDigitException


@dataclass(frozen=True)
class HashedPassword(Password, BaseValueObject[bytes]):
    value: bytes

    def validate(self): ...


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise EmailRequiredException

        if not re.fullmatch(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', self.value):
            raise InvalidEmailException(self.value)
