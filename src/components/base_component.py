from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from engine import Engine


class BaseComponent:
    """
    Base class for all components.
    """
    entity: Entity  # Owning entity instance

    @property
    def engine(self) -> Engine:
        """
        Shortcut to return the engine this entity belongs to.
        :return:
        """
        return self.entity.game_map.engine
