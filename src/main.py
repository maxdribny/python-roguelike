"""Author: Maxim Dribny 2023"""
import copy

import tcod

from engine.dungeon_gen import generate_dungeon
from engine.engine import Engine
from entities import entity_factories

RESOURCE_PATH = "..\\assets\\"


def main():
    """
    Sets up a game window using the tcod library, loads a tileset, and displays
    an @ symbol on the screen. The function waits for a QUIT event and exits the
    program if one is detected.

    :return: None
    """

    # region: Game Constants
    # These constants are used to define the size of the game window and the size of the map.
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    # endregion

    # region: Tile set and Graphics Options
    tileset = tcod.tileset.load_tilesheet(
        f"{RESOURCE_PATH}dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    # endregion:

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    # Generate a dungeon map
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine
    )

    engine.update_fov()

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Python Roguelike",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
