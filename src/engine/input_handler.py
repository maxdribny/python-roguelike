"""
The input handler file.
"""

from typing import Optional

import tcod.event

# TODO: this is a nasty import, figure this out later.
from commands.actions import *


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(dx=1, dy=0)

            # Add support for WASD movement
        elif key == tcod.event.K_w:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_s:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_a:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_d:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_z:
            action = UndoAction()

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action
