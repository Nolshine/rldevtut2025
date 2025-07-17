from typing import Optional, Protocol

import tcod.event

from actions import Action, EscapeAction, MovementAction
from config.input import movement_keys



class State(Protocol):
    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        ...


class DefaultState():
    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym) -> Optional[Action]:
        if sym in movement_keys:
            return MovementAction(*movement_keys[sym])
        if sym == tcod.event.KeySym.ESCAPE:
            return EscapeAction()
