from typing import Protocol, Optional

import tcod

from actions.actions import Action


class State(Protocol):
    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        ...
