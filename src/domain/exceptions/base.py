from dataclasses import dataclass


@dataclass
class DomainException(Exception):
    @property
    def message(self):
        return 'Доменная ошибка'
