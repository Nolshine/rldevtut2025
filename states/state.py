from __future__ import annotations
from typing import Protocol, Optional, TYPE_CHECKING

import tcod

if TYPE_CHECKING:
    from actions.action import Action


class State(Protocol):
    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        ...
