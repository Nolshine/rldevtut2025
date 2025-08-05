from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.entity import Entity

class EscapeAction:
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit

@attrs.define()
class MovementAction:
    dx: int
    dy: int

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x: int = entity.x + self.dx
        dest_y: int = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.is_walkable(dest_x, dest_y):
            return
        if engine.game_map.get_blocking_entity(dest_x, dest_y) is not None:
            return # We tried to move into an occupied space TODO: raise exception

        entity.move(self.dx, self.dy)

@attrs.define()
class MeleeAction:
    dx: int
    dy: int

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x: int = entity.x + self.dx
        dest_y: int = entity.y + self.dy
        target: Optional[Entity] = engine.game_map.get_blocking_entity(dest_x, dest_y)

        if target is None:
            return # We tried to melee but the entity doesn't exist TODO: raise exception

        print(f"You kick the {target.name}. It's not pleased.")

@attrs.define()
class BumpAction:
    dx: int
    dy: int

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x: int = entity.x + self.dx
        dest_y: int = entity.y + self.dy
        target: Optional[Entity] = engine.game_map.get_blocking_entity(dest_x, dest_y)

        if target is None:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
