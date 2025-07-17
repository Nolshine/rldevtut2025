import tcod.event

movement_keys: dict[tcod.event.KeySym, tuple[int, int]] = {
    tcod.event.KeySym.KP_8: (0, -1),     # up
    tcod.event.KeySym.KP_9: (1, -1),     # up-right
    tcod.event.KeySym.KP_6: (1, 0),      # right
    tcod.event.KeySym.KP_3: (1, 1),      # down-right
    tcod.event.KeySym.KP_2: (0, 1),      # down
    tcod.event.KeySym.KP_1: (-1, 1),     # down-left
    tcod.event.KeySym.KP_4: (-1, 0),     # left
    tcod.event.KeySym.KP_7: (-1, -1),    # up-left
}
