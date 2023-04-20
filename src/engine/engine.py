"""
Author: Maxim Dribny
"""

from typing import Set, Iterable, Any, List

from tcod.console import Console
from tcod.context import Context

from commands.actions import Action
from engine.game_map import GameMap
# noinspection PyUnresolvedReferences
from engine.input_handler import EventHandler
from entities.entity import Entity


class Engine:
    """
    The engine is the main class of the game.
    """

    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.action_stack: List[Action] = []

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

            action.perform(self, self.player)

            # --------------------------------------------------------------------
            # The below is code which was added as functionality to allow the player to undo their last action.
            # This is a very basic implementation of undo functionality.
            # --------------------------------------------------------------------
            if action.record_in_history:
                self.action_stack.append(action)  # Add the action to the action stack
                print(f"Action stack size: {len(self.action_stack)}")
                # Limit the undo stack size to 32 actions
                if len(self.action_stack) > 32:
                    self.action_stack.pop(0)

    def undo_last_action(self) -> None:
        """
        Undo the last action performed by the player.
        :return: None
        """

        if not self.action_stack:
            return

        last_action = self.action_stack.pop()
        print(f"Action stack size: {len(self.action_stack)}")
        last_action.undo(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        """
        Render the entities to the console.
        :param console:
        :param context:

        :return: None
        """
        self.game_map.render(console)

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)

        console.clear()
