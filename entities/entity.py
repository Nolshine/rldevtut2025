from __future__ import annotations

import attrs

import copy
from typing import TYPE_CHECKING

from config import theme

if TYPE_CHECKING:
    from game_map.game_map import GameMap

# NOTE: All instances of Entity are going to be unique and not equal each other.
#       This is because they will be compared and hashed using their IDs.
#       `attrs` would normally make them compared (and hashed) by their attributes by default,
#       but because an Entity is mutable, that would make them unhashable.
#       Further reading: https://hynek.me/articles/hashes-and-equality/
@attrs.define(eq=False)
class Entity:
    """
    A generic in-game entity. Functionality is decided by which components are enabled.
    """
    x: int = 0
    y: int = 0
    char: str = "?"
    color: tuple[int, int, int] = theme.white
    name: str = "<Unnamed>"
    blocks_movement: bool = False

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def spawn(self: Entity, game_map: GameMap, x: int, y: int) -> Entity:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        game_map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        """
        Change the entity's position by the given amounts.
        """
        self.x += dx
        self.y += dy
