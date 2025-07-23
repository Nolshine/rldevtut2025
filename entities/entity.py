class Entity:
    """
    A generic in-game entity. Functionality is decided by which components are enabled.
    """
    x: int
    y: int
    char: str
    color: tuple[int, int, int] # (r, g, b)

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __init__(self, x: int, y: int, char: str, color: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        """
        Change the entity's position by the given amounts.
        """
        self.x += dx
        self.y += dy
