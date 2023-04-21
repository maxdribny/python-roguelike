"""
This module contains the GameMap class.
"""

import numpy as np  # type: ignore
from tcod.console import Console

from engine import tile_types


class GameMap:
    """
    A generic map. Should be subclassed or used as a component.
    """

    def __init__(self, width: int, height: int):
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

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

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
