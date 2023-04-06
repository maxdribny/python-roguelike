from typing import Tuple

from engine import tile_types
from engine.game_map import GameMap


class RectangularRoom:
    """
    A rectangular room on a two-dimensional grid.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """
        Return the center coordinates of this room.
        :return: Tuple[int, int] The center coordinates of this room.
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
        Return the inner area of this room as a 2D array index.
        :return: Tuple[slice, slice] The inner area of this room.
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


def generate_dungeon(map_width, map_height) -> GameMap:
    """
    Generate a new dungeon map.
    :param map_width: int The width of the map.
    :param map_height: int The height of the map.
    :return: GameMap The generated dungeon map.
    """
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    return dungeon
