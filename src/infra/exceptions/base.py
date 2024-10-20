from src.domain.exceptions.base import DomainException


class InfraException(DomainException):
    @property
    def message(self):
        return 'Инфраструктурная ошибка'
