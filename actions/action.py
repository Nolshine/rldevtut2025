from __future__ import annotations
from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from engine.engine import Engine
    from entities.entity import Entity


class Action(Protocol):
    def perform(self, engine: Engine, entity: Entity) -> None:
        ...
