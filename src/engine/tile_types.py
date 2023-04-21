"""
Author: Maxim Dribny
Copyright: 2023

This module provides the data structure and helper functions for managing tiles in a console-based Roguelike game.
"""

from typing import Tuple

import numpy as np

# Tiles graphics structured type compatible with Console.rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors - foreground
        ("bg", "3B"),  # 3 unsigned bytes, for RGB colors - background
    ]
)

# Tile struct / datatype used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # True if this tile can be walked over
        ("transparent", np.bool_),  # True if this tile doesn't block FOV
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV
        ("light", graphic_dt),  # Graphics for when this tile is in FOV
    ]
)


def new_tile(
        *,  # Enforce the use of keywords, so that parameter order doesn't matter
        walkable: bool,
        transparent: bool,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """
    Create a new tile with the specified properties.

    This helper function returns a NumPy array with the given tile data,
    using the specified dtype (tile_dt).

    Keyword Arguments:
    walkable (int): The walk-ability of the tile (True or False).
    transparent (int): The transparency of the tile (True or False).
    dark (Tuple): A tuple containing the Unicode codepoint of the tile's
                  character, the foreground color as an RGB tuple, and the
                  background color as an RGB tuple.

    Returns:
    np.ndarray: A NumPy array containing the tile data.

    :keyword walkable: The walk ability of the tile (True or False).
    :keyword transparent: The transparency of the tile (True or False).
    :keyword dark: A tuple containing the Unicode codepoint of the tile's character,
    the foreground color as an RGB tuple, and the background color as an RGB tuple.

    :return: A NumPy array containing the tile data.
    """

    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles.
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# ------------------------------------------------------------
# TYPES OF TILES:
# Floor: Walkable: True, Transparent: True, Dark: No Character, White Foreground, Blue Background
# Wall: Walkable: False, Transparent: False, Dark: No Character, White Foreground, Dark Blue Background
# ------------------------------------------------------------

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)
