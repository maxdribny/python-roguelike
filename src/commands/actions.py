"""
Copyright: 2023.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.entity import Entity


class Action:
    """
    An action is a command that can be performed by an entity.
    """
    prev_state: dict

    def __init__(self):
        self.record_in_history = True

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        :param engine: Engine The scope of this action.
        :param entity: Entity The object performing the action.

        :return: None
        """
        self.prev_state = self.save_state(entity)  # Save the state before performing the action.
        raise NotImplementedError()

    def undo(self, engine: Engine, entity: Entity) -> None:
        """
        Undo the action by restoring the entity to the state it was in before the action was performed.
        :param engine: Engine The scope of this action.
        :param entity: Entity The entity to restore the state of.

        :return: None
        """
        raise NotImplementedError()

    def save_state(self, entity: Entity) -> dict:
        """
        Save the state of the entity before performing the action.
        :param entity: Entity The entity to save the state of.

        :return: dict The state of the entity.
        """
        return {
            "x": entity.x,
            "y": entity.y,
        }


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
        # Save the state before performing the action.
        prev_state = self.save_state(entity)

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

        # Store the previous state in the entity.
        self.prev_state = prev_state

    def undo(self, engine: Engine, entity: Entity) -> None:
        # Restore the entity to the state it was in before the action was performed.
        entity.x = self.prev_state["x"]
        entity.y = self.prev_state["y"]


class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)


class UndoAction(Action):
    """
    An action to undo the last action performed by the player.
    """

    def __init__(self):
        super().__init__()
        self.record_in_history = False

    def perform(self, engine: Engine, entity: Entity) -> None:
        engine.undo_last_action()

    def undo(self, engine: Engine, entity: Entity) -> None:
        pass


class EscapeAction(Action):
    """
    An action to exit the game.
    """

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()
