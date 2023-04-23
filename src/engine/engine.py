"""Author: Maxim Dribny 2023"""

from typing import Iterable, Any

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from engine.game_map import GameMap
from engine.input_handler import EventHandler
from entities.entity import Entity


class Engine:
    """
    The main game engine class that holds and operates on the game state.
    """

    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        """
        Initializes a new Engine object.
        :param player: Entity The player entity.
        """
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        """
        Handle the turns of all entities that are not the player.
        """
        for entity in self.game_map.entities - {self.player}:
            print(f"The {entity.name} wonders when it will get to take a real turn.")

    def handle_events(self, events: Iterable[Any]) -> None:
        """
        Handle events from the input handler.
        :param events:
        """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.handle_enemy_turns()
            self.update_fov()  # Update the FOV before the players next action.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """
        Render the entities to the console.
        :param console:
        :param context:

        :return: None
        """
        self.game_map.render(console)

        context.present(console)

        console.clear()
