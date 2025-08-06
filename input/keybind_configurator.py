from typing import TypeAlias
import pathlib
import pickle

import attrs

import tcod.event

from config.input import KEYBINDS_PATH, DEFAULT_KEYBINDS_PATH

MovementKeyConfig: TypeAlias = dict[tcod.event.KeySym, tuple[int, int]]

@attrs.define
class KeybindConfigurator:
    movement_keys: MovementKeyConfig
    # wait_keys: list[tcod.event.KeySym]
    # system_keys: TBD

    # TODO: Figure out a sensible way to store multiple categories of keys in one file

    @classmethod
    def first_load(cls) -> "KeybindConfigurator":
        # determine if a user-defined set of keybinds exists
        if KEYBINDS_PATH.exists():
            return cls(movement_keys=cls.load(KEYBINDS_PATH))
        else:
            return cls(movement_keys=cls.load(DEFAULT_KEYBINDS_PATH))

    @classmethod
    def load(cls, path: pathlib.Path) -> MovementKeyConfig:
        # NOTE: atm will only load the move keys dictionary
        mv_keys: MovementKeyConfig
        with open(path, 'rb') as f:
            mv_keys = pickle.load(f)
        return mv_keys

    def save(self, path: pathlib.Path) -> None:
        raise NotImplementedError
