import tcod

RESOURCE_PATH = "assets\\"


def main():
    """
    Sets up a game window using the tcod library, loads a tileset, and displays
    an @ symbol on the screen. The function waits for a QUIT event and exits the
    program if one is detected.

    :return: None
    """
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        f"{RESOURCE_PATH}dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Python Roguelike",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()
