import tcod

from commands.actions import MovementAction, EscapeAction
from engine.input_handler import EventHandler
from entities.entity import Entity

RESOURCE_PATH = "..\\assets\\"


def main():
    """
    Sets up a game window using the tcod library, loads a tileset, and displays
    an @ symbol on the screen. The function waits for a QUIT event and exits the
    program if one is detected.

    :return: None
    """
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        f"{RESOURCE_PATH}dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    # Added support for entities instead of hard coded player

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Python Roguelike",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)

            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
