"""
Copyright: 2023.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from engine.engine import Engine


class Action:
    """
    An action is a command that can be performed by an entity.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.
        'self.engine' is the scope this action is being performed in.
        'self.entity' is the object performing the action.

        This method must be overriden by Action subclasses.

        :return: None
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """
    An action to exit the game.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)

        if not target:
            return  # No entity to attack

        print(f"You kick the {target.name} in the balls!")


class MovementAction(ActionWithDirection):
    """
    An action to move an entity.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:

        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        # Otherwise move
        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
