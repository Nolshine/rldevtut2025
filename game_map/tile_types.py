import numpy as np

from config import theme



graphic_dt = np.dtype(
    [
        ("ch", np.int32), # Unicode codepoint
        ("fg", "3B"), # 3 Unsigned bytes for RGB Colours
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("dark", graphic_dt), # Not in FOV
        ("light", graphic_dt), # In FOV
    ]
)

def new_tile(
        *, #Enforce the use of keywords so param order doesn't matter
        walkable: bool,
        transparent: bool,
        dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
        light: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types."""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), theme.dark_blue, theme.black),
    light=(ord("."), theme.light_blue, theme.black),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), theme.dark_grey, theme.black),
    light=(ord("#"), theme.white, theme.black),
)
