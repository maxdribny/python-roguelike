"""Author: Maxim Dribny 2023"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from engine.input_handler import EventHandler

if TYPE_CHECKING:
    from entities.entity import Entity
    from engine.game_map import GameMap


class Engine:
    """
    The main game engine class that holds and operates on the game state.
    """

    game_map: GameMap

    def __init__(self, player: Entity):
        """
        Initializes a new Engine object.
        :param player: Entity The player entity.
        """
        self.event_handler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        """
        Handle the turns of all entities that are not the player.
        """
        for entity in self.game_map.entities - {self.player}:
            print(f"The {entity.name} wonders when it will get to take a real turn.")

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
