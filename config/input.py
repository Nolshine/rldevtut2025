import pickle
import pathlib

import tcod.event

KEYBINDS_PATH: pathlib.Path = pathlib.Path("config/keybinds.cfg")
DEFAULT_KEYBINDS_PATH: pathlib.Path = pathlib.Path("config/default_keybinds.cfg")

class KeybindConfigurator:
    movement_keys: dict[tcod.event.KeySym, tuple[int, int]]
    # wait_keys: list[tcod.event.KeySym]
    # system_keys: TBD

    # TODO: Figure out a sensible way to store multiple categories of keys in one file

    def __init__(self):
        # determine if a user-defined set of keybinds exists
        if KEYBINDS_PATH.exists():
            self.load(KEYBINDS_PATH)
        else:
            self.load(DEFAULT_KEYBINDS_PATH)

    def load(self, path: pathlib.Path) -> None:
        # NOTE: atm will only load the move keys dictionary
        with open(path, 'rb') as f:
            self.movement_keys = pickle.load(f)

    def save(self, path: pathlib.Path) -> None:
        raise NotImplementedError
