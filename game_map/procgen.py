from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

import random

from tcod.los import bresenham

from game_map.game_map import GameMap
import game_map.tile_types as tile_types

if TYPE_CHECKING:
    from entities.entity import Entity



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

    def intersects(self, other: RectangularRoom) -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between(
        start: tuple[int, int],
        end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between the `start` and `end` points."""
    x1, y1 = start
    x2, y2 = end

    corner_x: int
    corner_y: int

    if random.random() < 0.5:
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


def basic_generator(
        map_width: int,
        map_height: int,
        room_min_size: int,
        room_max_size: int,
        max_rooms: int,
        player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    rooms: list[RectangularRoom] = []

    for r in range(max_rooms): # type ignore
        print(rooms)
        room_width: int = random.randint(room_min_size, room_max_size)
        room_height: int = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # intersection; throw away room

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # This is the first room, place the player inside it
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon
