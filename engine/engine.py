from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
import tcod.event

from game_map.game_map import GameMap
from game_map.procgen import basic_generator

if TYPE_CHECKING:
    from states.state import State
    from entities.entity import Entity
    from actions.action import Action

class Engine:
    game_map: GameMap
    entities: set[Entity]
    current_state: State
    player: Entity

    def __init__(self, entities: set[Entity], initial_state: State, player: Entity) -> None:
        self.entities = entities
        self.current_state = initial_state
        self.player = player

    def new_map(self, width: int, height: int, room_min_size: int, room_max_size: int, max_rooms: int) -> None: # eventually, the desired generator will be fed in as a parameter.
        self.game_map = basic_generator(width, height, room_min_size, room_max_size, max_rooms, self.player)

    def update(self, events: Iterable[tcod.event.Event]) -> None:
        # block by listening to input here
        # and processing player turn
        for event in events:
            action: Optional[Action] = self.current_state.on_event(event)

            if action is None:
                    continue

            action.perform(self, self.player)
        # follow with all AI turns

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)

        context.present(console=console, integer_scaling=True)
        console.clear()
