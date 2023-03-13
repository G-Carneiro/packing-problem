from __future__ import annotations


class Coordinate:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __lt__(self, other: Coordinate) -> bool:
        if (self.x != other.x):
            return (self.x < other.x)

        return (self.y < other.y)
