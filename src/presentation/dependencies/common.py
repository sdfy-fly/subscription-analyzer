from src.application.mediator import Mediator
from src.core.container import get_container


def get_mediator() -> Mediator:
    container = get_container()
    return container.resolve(Mediator)
