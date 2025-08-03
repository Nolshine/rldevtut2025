#!/usr/bin/env python3
import tcod

from config.engine import SCREEN_WIDTH, SCREEN_HEIGHT, TILESHEET, TILESHEET_COLS, TILESHEET_ROWS
from config.map import MAP_WIDTH, MAP_HEIGHT, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAX_ROOMS
from config.input import KeybindConfigurator

from states.state import State
from states.game_states import DefaultState
from entities.entity import Entity
from engine.engine import Engine
from game_map.procgen import basic_generator


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
    game_map = basic_generator(
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        room_min_size=ROOM_MIN_SIZE,
        room_max_size=ROOM_MAX_SIZE,
        max_rooms=MAX_ROOMS,
        player=player,
    )
    engine = Engine(initial_state, game_map, player)

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
