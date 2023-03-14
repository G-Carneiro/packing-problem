from __future__ import annotations


class Coordinate:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __lt__(self, other: Coordinate) -> bool:
        if (self.x != other.x):
            return (self.x < other.x)

        return (self.y < other.y)

    def __eq__(self, other: Coordinate | tuple[float, float]) -> bool:
        if isinstance(other, tuple):
            other = Coordinate(other[0], other[1])

        return (self.x == other.x and self.y == other.y)

    def __le__(self, other: Coordinate) -> bool:
        return (self < other or self == other)

    def __add__(self, other: Coordinate | tuple[float, float]) -> Coordinate:
        if isinstance(other, tuple):
            other = Coordinate(other[0], other[1])

        return Coordinate(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
