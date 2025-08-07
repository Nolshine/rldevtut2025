from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

import attrs

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

@attrs.define
class Engine:
    current_state: State
    game_map: GameMap
    player: Entity

    def __attrs_post_init__(self) -> None: # pyright: ignore[reportUnusedFunction]
         self.update_fov()

    def update(self, events: Iterable[tcod.event.Event]) -> None:
        # block by listening to input here
        # and processing player turn
        for event in events:
            action: Optional[Action] = self.current_state.on_event(event)

            if action is not None:
                action.perform(self, self.player)
                self.handle_enemy_turns()
                self.update_fov()

    def handle_enemy_turns(self) -> None:
         for ent in self.game_map.entities - {self.player}:
              print(f"The {ent.name} wonders when it will get to have a real turn.")


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

        context.present(console=console, integer_scaling=True)
        console.clear()
