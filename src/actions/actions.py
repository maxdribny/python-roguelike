"""
Author: maxdribny
"""


class Action:
    """
    An action is an action that can be acted on in the game world.
    Forms the base class for other actions.
    """
    pass


class EscapeAction(Action):
    """
    An escape action is an action that exits the game.
    """
    pass


class MovementAction(Action):
    """
    A movement action is an action that moves the entity by a certain amount.
    """

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
