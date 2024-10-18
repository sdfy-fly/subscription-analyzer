from dataclasses import dataclass, field

from src.application.commands.base import CR, BaseCommand, BaseCommandHandler
from src.application.exceptions.mediator import CommandHandlerNotFound


@dataclass
class Mediator:
    commands_map: dict[type[BaseCommand], BaseCommandHandler] = field(default_factory=dict)

    def register_command(self, command: type[BaseCommand], handler: BaseCommandHandler) -> None:
        self.commands_map[command] = handler

    async def handle_command(self, command: BaseCommand) -> CR:
        command_type = command.__class__
        handler = self.commands_map.get(command_type)
        if not handler:
            raise CommandHandlerNotFound(command_type)

        return await handler.handle(command)
