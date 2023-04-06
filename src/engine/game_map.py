import numpy as np  # type: ignore
from tcod.console import Console

from engine import tile_types


class GameMap:
    """
    A generic map. Should be subclassed or used as a component.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Return True if x and y are inside the bounds of this map.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.
        :param console:
        """
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
