from __future__ import annotations

from typing import Iterable, Optional,  TYPE_CHECKING

import attrs

import numpy as np
from tcod.console import Console

import game_map.tile_types as tile_types

if TYPE_CHECKING:
    from entities.entity import Entity

@attrs.define
class GameMap:
    width: int
    height: int
    tiles: np.ndarray
    visible: np.ndarray
    explored: np.ndarray
    entities: set[Entity]

    @classmethod
    def new(cls, width: int, height: int, entities: Iterable[Entity] = ()) -> "GameMap":
        tiles = np.full(shape=(width, height), fill_value=tile_types.wall)
        visible = np.full(shape=(width, height), fill_value=False)
        explored = np.full(shape=(width, height), fill_value=False)

        entities_set = set(entities)
        return cls(width=width, height=height, tiles=tiles, visible=visible, explored=explored, entities=entities_set)

    def in_bounds(self, x: int, y: int) -> bool:
        """Returns true if given position is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        return self.tiles[x, y]["walkable"]

    def get_blocking_entity(self, x: int, y: int) -> Optional[Entity]:
        for ent in self.entities:
            if not (ent.x == x and ent.y == y):
                continue
            elif ent.blocks_movement:
                return ent
        return None

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
