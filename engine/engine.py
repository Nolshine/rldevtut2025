from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
import tcod.event

from game_map.game_map import GameMap

from config.gameplay import PLAYER_FOV_RADIUS

if TYPE_CHECKING:
    from states.state import State
    from entities.entity import Entity
    from actions.action import Action

class Engine:
    game_map: GameMap
    entities: set[Entity]
    current_state: State
    player: Entity

    def __init__(self, entities: set[Entity], initial_state: State, game_map: GameMap, player: Entity) -> None:
        self.entities = entities
        self.current_state = initial_state
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def update(self, events: Iterable[tcod.event.Event]) -> None:
        # block by listening to input here
        # and processing player turn
        for event in events:
            action: Optional[Action] = self.current_state.on_event(event)

            if action is None:
                    continue

            action.perform(self, self.player)
        # follow with all AI turns
        self.update_fov()

    def update_fov(self) -> None:
        """
        Updates the player's field of vision, marking tiles within the player's FOV radius as visible.
        Tiles previously visible that are now no longer in FOV will remain explored.
        """
        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=self.player.position,
            radius=PLAYER_FOV_RADIUS,
        )
        # Given tile is `explored` if its position in `explored` is `True` OR its position in `visible` is `True`
        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            if not self.game_map.visible[entity.x, entity.y]:
                continue
            console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)

        context.present(console=console, integer_scaling=True)
        console.clear()
