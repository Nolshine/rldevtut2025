from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import game_map.tile_types as tile_types

if TYPE_CHECKING:
    from entities.entity import Entity


class GameMap:
    width: int
    height: int
    visible: np.ndarray
    explored: np.ndarray
    entities: set[Entity]

    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()) -> None:
        self.width, self.height = width, height

        self.tiles = np.full(shape=(width, height), fill_value=tile_types.wall)
        self.visible = np.full(shape=(width, height), fill_value=False)
        self.explored = np.full(shape=(width, height), fill_value=False)

        self.entities = set(entities)

    def in_bounds(self, x: int, y: int) -> bool:
        """Returns true if given position is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        return self.tiles[x, y]["walkable"]

    def render(self, console: Console) -> None:
        """
        Renders the map.

        `visible` tiles will be rendered using the "light" `graphic_dt`.
        Tiles not `visible` that are still `explored` will be rendered with the "dark" `graphic_dt`.
        Tiles not `visible` nor `explored` will be rendered as SHROUD.
        """
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            if not self.visible[entity.x, entity.y]:
                continue
            console.print(
                x=entity.x,
                y=entity.y,
                text=entity.char,
                fg=entity.color
            )
