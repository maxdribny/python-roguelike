"""
Author: Maxim Dribny
"""

from typing import Set, Iterable, Any

from tcod.console import Console
from tcod.context import Context

from commands.actions import MovementAction, EscapeAction
# noinspection PyUnresolvedReferences
from engine.input_handler import EventHandler
from entities.entity import Entity


class Engine:
    """
    The engine is the main class of the game.
    """

    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        """
        Handle events from the event handler.
        :param events: Iterable[Any] The events to handle.

        :return: None
        """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        """
        Render the entities to the console.
        :param console:
        :param context:

        :return: None
        """
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)

        console.clear()
