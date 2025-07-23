from typing import Optional

import tcod.event

from actions.actions import Action, EscapeAction, MovementAction


class DefaultState:
    mv_keys: dict[tcod.event.KeySym, tuple[int, int]]

    def __init__(self, movement_keys: dict[tcod.event.KeySym, tuple[int, int]]):
        self.mv_keys = movement_keys

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym) -> Optional[Action]:
        if sym in self.mv_keys:
            return MovementAction(*self.mv_keys[sym])
        if sym == tcod.event.KeySym.ESCAPE:
            return EscapeAction()
