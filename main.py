#!/usr/bin/env python3
import tcod

from config.engine import SCREEN_WIDTH, SCREEN_HEIGHT, TILESHEET, TILESHEET_COLS, TILESHEET_ROWS
from config.input import KeybindConfigurator

from states.state import State
from states.game_states import DefaultState
from entities.entity import Entity
from engine.engine import Engine


def main() -> None:
    kb_config: KeybindConfigurator = KeybindConfigurator()
    initial_state: State = DefaultState(kb_config.movement_keys)

    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        TILESHEET,
        TILESHEET_COLS,
        TILESHEET_ROWS,
        tcod.tileset.CHARMAP_TCOD,
    )

    player: Entity = Entity(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "@", (255, 255, 255))
    npc: Entity = Entity(player.x + 3, player.y, "@", (255, 255, 150))
    entities = {player, npc}

    engine: Engine = Engine(entities, initial_state, player)
    engine.new_map(SCREEN_WIDTH, SCREEN_HEIGHT)

    with tcod.context.new(
        columns=SCREEN_WIDTH,
        rows=SCREEN_HEIGHT,
        tileset=tileset,
        title="2025 is the year where it's really a roguelike",
        vsync=True,
        sdl_window_flags=tcod.context.SDL_WINDOW_MAXIMIZED | tcod.context.SDL_WINDOW_RESIZABLE #type: ignore
    ) as context:
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            engine.render(root_console, context)
            engine.update(tcod.event.wait())



if __name__ == "__main__":
    main()
