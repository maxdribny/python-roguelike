"""
This module contains the GameMap class.
"""
from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from engine import tile_types

if TYPE_CHECKING:
    from entities.entity import Entity


class GameMap:
    """
    A generic map. Should be subclassed or used as a component.
    """

    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        """
        Initializes a new GameMap object with specified width and height.

        Args:
            width (int): The width of the GameMap object.
            height (int): The height of the GameMap object.

        Returns:
            None
        """
        self.width = width
        self.height = height

        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        """
        Returns the blocking entity at the given location, if one exists.

        Args:
            location_x (int): The x coordinate to check.
            location_y (int): The y coordinate to check.

        Returns:
            Optional[Entity]: The blocking entity at the given location, if one exists.
            None: If no blocking entity is found at the given location.
        """
        
        # TODO: Modify this so that we only check the entities within a given radius as the game map may become large
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Returns True if the given x and y coordinates are within the bounds of the map.

        Args:
            x (int): The x coordinate to check.
            y (int): The y coordinate to check.

        Returns:
            bool: True if x and y are inside the bounds of this map, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map onto the given console.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".

        Args:
            console (Console): The console to render the map onto.

        Returns:
            None
        """
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only render entities that are in the visible area.
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
