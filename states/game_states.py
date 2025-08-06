from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import attrs

import tcod.event

from actions.actions import EscapeAction, BumpAction

if TYPE_CHECKING:
    from actions.action import Action


@attrs.define
class DefaultState:
    mv_keys: dict[tcod.event.KeySym, tuple[int, int]]

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
            return BumpAction(*self.mv_keys[sym])
        if sym == tcod.event.KeySym.ESCAPE:
            return EscapeAction()
