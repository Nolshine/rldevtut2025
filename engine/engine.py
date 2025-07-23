from typing import Iterable, Optional

from tcod.context import Context
from tcod.console import Console
import tcod.event

from actions.actions import Action, EscapeAction, MovementAction
from entities.entity import Entity
from states.state import State


class Engine:
    entities: set[Entity]
    current_state: State
    player: Entity

    def __init__(self, entities: set[Entity], initial_state: State, player: Entity) -> None:
        self.entities = entities
        self.current_state = initial_state
        self.player = player

    def update(self, events: Iterable[tcod.event.Event]) -> None:
        # block by listening to input here
        # and processing player turn
        for event in events:
            action: Optional[Action] = self.current_state.on_event(event)

            if action is None:
                    continue

            if isinstance(action, MovementAction):
                self.player.move(action.dx, action.dy)

            if isinstance(action, EscapeAction):
                raise SystemExit
        # follow with all AI turns

    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)

        context.present(console)
        console.clear()
