from dataclasses import dataclass, field

from src.application.commands.base import CR, BaseCommand, BaseCommandHandler
from src.application.exceptions.mediator import CommandHandlerNotFound, QueryHandlerNotFound
from src.application.queries.base import QR, BaseQuery, BaseQueryHandler


@dataclass
class Mediator:
    _commands_map: dict[type[BaseCommand], BaseCommandHandler] = field(default_factory=dict)
    _queries_map: dict[type[BaseQuery], BaseQueryHandler] = field(default_factory=dict)

    def register_command(self, command: type[BaseCommand], handler: BaseCommandHandler) -> None:
        self._commands_map[command] = handler

    def register_query(self, query: type[BaseQuery], handler: BaseQueryHandler) -> None:
        self._queries_map[query] = handler

    async def handle_command(self, command: BaseCommand) -> CR:
        command_type = command.__class__
        handler = self._commands_map.get(command_type)
        if not handler:
            raise CommandHandlerNotFound(command_type)

        return await handler.handle(command)

    async def handle_query(self, query: BaseQuery) -> QR:
        query_type = query.__class__
        handler = self._queries_map.get(query_type)
        if not handler:
            raise QueryHandlerNotFound(query_type)

        return await handler.handle(query)
