from entities.entity import Entity
from config import theme


player = Entity(char="@", color=theme.white, name="Player", blocks_movement=True)

orc = Entity(char="o", color=theme.orc, name="Orc", blocks_movement=True)
troll = Entity(char="T", color=theme.troll, name="Troll", blocks_movement=True)
