from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.entity import Entity

class EscapeAction:
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit


class MovementAction:
    def __init__(self, dx: int, dy: int) -> None:
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x: int = entity.x + self.dx
        dest_y: int = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.is_walkable(dest_x, dest_y):
            return

        entity.move(self.dx, self.dy)
