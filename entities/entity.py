from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from config import theme

if TYPE_CHECKING:
    from game_map.game_map import GameMap



class Entity:
    """
    A generic in-game entity. Functionality is decided by which components are enabled.
    """
    x: int
    y: int
    char: str
    color: tuple[int, int, int] # (r, g, b)
    name: str
    blocks_movement: bool

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: tuple[int, int, int] = theme.white,
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

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
