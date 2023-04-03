from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.entity import Entity


class Action:
    """
    An action is a command that can be performed by an entity.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        :param engine: Engine The scope of this action.
        :param entity: Entity The object performing the action.

        :return: None
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    An action to exit the game.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):
    """
    An action to move an entity.
    """

    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        # Otherwise move
        entity.move(self.dx, self.dy)
