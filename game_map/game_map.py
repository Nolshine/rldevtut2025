import numpy as np
from tcod.console import Console

import game_map.tile_types as tile_types



class GameMap:
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.tiles = np.full(shape=(width, height), fill_value=tile_types.floor)

        self.tiles[30:33, 22] = tile_types.wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Returns true if given position is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = self.tiles["dark"]
