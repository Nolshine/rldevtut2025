from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

import random

import attrs

from tcod.los import bresenham

from game_map.game_map import GameMap
import game_map.tile_types as tile_types
from entities import entity_factories

if TYPE_CHECKING:
    from entities.entity import Entity


@attrs.define
class RectangularRoom:
    x1: int
    x2: int
    y1: int
    y2: int

    @classmethod
    def by_size(cls, x: int, y: int, width: int, height: int) -> "RectangularRoom":
        return cls(x1=x, x2=x+width, y1=y, y2=y+height)


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

def place_entities(
        room: RectangularRoom,
        dungeon: GameMap,
        max_monsters: int,
) -> None:
    num_monsters = random.randint(0, max_monsters)

    for i in range(num_monsters): #type: ignore
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                entity_factories.troll.spawn(dungeon, x, y)

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
        max_monsters_per_room: int,
        player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: list[RectangularRoom] = []

    for r in range(max_rooms): # type: ignore
        room_width: int = random.randint(room_min_size, room_max_size)
        room_height: int = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom.by_size(x=x, y=y, width=room_width, height=room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # intersection; throw away room

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # This is the first room, place the player inside it
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room)

        rooms.append(new_room)

    return dungeon
