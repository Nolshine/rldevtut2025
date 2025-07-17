#!/usr/bin/env python3
from typing import Optional

import tcod

from config.engine import SCREEN_WIDTH, SCREEN_HEIGHT, TILESHEET, TILESHEET_COLS, TILESHEET_ROWS

from input_handlers import State, DefaultState
from actions import Action, MovementAction, EscapeAction


def main() -> None:
    state: State = DefaultState()

    tileset: tcod.tileset.Tileset = tcod.tileset.load_tilesheet(
        TILESHEET,
        TILESHEET_COLS,
        TILESHEET_ROWS,
        tcod.tileset.CHARMAP_TCOD,
    )

    player_x: int = int(SCREEN_WIDTH/2)
    player_y: int = int(SCREEN_HEIGHT/2)

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
            root_console.clear()
            root_console.print(x=player_x, y=player_y, text="@")

            context.present(root_console, integer_scaling=True)

            action: Optional[Action] = None

            for event in tcod.event.wait():
                print(event)
                action = state.on_event(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction): # TODO: make intellisense see 'action' as only MovementAction here
                    player_x += action.dx
                    player_y += action.dy

                if isinstance(action, EscapeAction):
                    raise SystemExit



if __name__ == "__main__":
    main()
