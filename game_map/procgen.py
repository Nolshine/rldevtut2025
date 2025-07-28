from typing import Iterator
from random import random

from tcod.los import bresenham

from game_map.game_map import GameMap
import game_map.tile_types as tile_types



class RectangularRoom:
    x1: int
    x2: int
    y1: int
    y2: int

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

def tunnel_between(
        start: tuple[int, int],
        end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between the `start` and `end` points."""
    x1, y1 = start
    x2, y2 = end

    corner_x: int
    corner_y: int

    if random() < 0.5:
        # Dig horizontally, then vertically
        corner_x = x2
        corner_y = y1
    else:
        # Dig vertically, then horizontally
        corner_x = x1
        corner_y = y2

    for x, y in bresenham(start, (corner_x, corner_y)):
        yield x, y
    for x, y in bresenham((corner_x, corner_y), end):
        yield x, y


def basic_generator(map_width: int, map_height: int) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    for x, y in tunnel_between(room_1.center, room_2.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon
