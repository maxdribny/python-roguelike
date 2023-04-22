from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from engine import tile_types
from engine.game_map import GameMap
from entities import entity_factories

if TYPE_CHECKING:
    from entities.entity import Entity


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

    def intersects(self, other: RectangularRoom) -> bool:
        """
        Return True if this room overlaps with another RectangularRoom.
        :param other:
        :return: bool: True if the other room overlaps with this one, False otherwise.
        """
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def place_entities(room: RectangularRoom, dungeon: GameMap, max_monsters: int) -> None:
    """
    Place entities in a room.

    Args:
        room (RectangularRoom): The room in which to place entities.
        dungeon (GameMap): The dungeon map.
        max_monsters (int): The maximum number of monsters to place in the room.

    Note:
        This function randomly places monsters in the room. The number of monsters is determined by the 'max_monsters'
        parameter. The function ensures that the monsters are not placed on top of each other.

    Examples:
        >> place_entities(room, dungeon, max_monsters_per_room)
    """

    number_of_monsters = random.randint(0, max_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                entity_factories.troll.spawn(dungeon, x, y)


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """
    Return an L-shaped tunnel between the start and end points.

    Args:
        start (Tuple[int, int]): The starting point of the tunnel.
        end (Tuple[int, int]): The ending point of the tunnel.

    Returns:
        Iterator[Tuple[int, int]]: A generator that yields the x, y coordinates of each point along the tunnel path.

    Note:
        This function generates an L-shaped tunnel that starts either horizontally or vertically, and then proceeds in
        the other direction to reach the end point. The exact path of the tunnel is randomly determined. The tunnel is
        created using the Bresenham line algorithm from the python-tcod library.
    """
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel - ignore the warnings it works.

    # noinspection PyTypeChecker
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    # noinspection PyTypeChecker
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        max_monsters_per_room: int,
        player: Entity,
) -> GameMap:
    """
    Generate a new dungeon map with randomly placed rectangular rooms and tunnels connecting them.

    The function creates a 'GameMap' instance and populates it with 'RectangularRoom' instances. It ensures that the
    rooms do not intersect and connects them with tunnels. The player's starting position is set to the center of the
    first room.

    Args:
        max_rooms (int): The maximum number of rooms to generate.
        room_min_size (int): The minimum size (width and height) of a room.
        room_max_size (int): The maximum size (width and height) of a room.
        map_width (int): The width of the dungeon map.
        map_height (int): The height of the dungeon map.
        max_monsters_per_room (int): The maximum number of monsters that can be placed in a room.
        player (Entity): The player entity.

    Returns:
        GameMap: The generated dungeon map with rooms and tunnels.

    Raises:
        ValueError: If the maximum number of rooms is less than 1, room_min_size is less than 1 or room_max_size is less
        than room_min_size.

    Examples:
        >> player = Entity(0, 0, "@", (255, 255, 255)) \n
        >> dungeon = generate_dungeon(10, 5, 10, 80, 50, player) \n
        >> print(dungeon_map.width, dungeon_map.height) \n
        >> 80 50
    """

    if max_rooms < 1:
        raise ValueError("Maximum number of rooms must be greater than 0.")
    if room_min_size < 1:
        raise ValueError("Minimum room size must be greater than 0.")
    if room_max_size < room_min_size:
        raise ValueError("Maximum room size must be greater than or equal to minimum room size.")

    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    for room in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # Create a new rectangular room with the dimensions (random width and height and random position).
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Iterate through the other rooms and see if they intersect with the current room. If there are no
        #   intersections then the room is valid.
        # NOTE: This is runtime safe as, if there are no rooms which can fit within the map,
        #   the loop will eventually stop.

        if any(new_room.intersects(r) for r in rooms):
            continue  # This room intersects -> continue (skip the rest of the loop) to the next attempt.

        # Set the room's inner tiles to be floor.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts
            player.x, player.y = new_room.center
        else:
            # All rooms after the first.
            # Dig a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Place monsters in the room.
        place_entities(new_room, dungeon, max_monsters_per_room)

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
