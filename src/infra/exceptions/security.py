from src.infra.exceptions.base import InfraException


class InvalidJwt(InfraException):
    @property
    def message(self):
        return 'Неверный jwt токен!'
