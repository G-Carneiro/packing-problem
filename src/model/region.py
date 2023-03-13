from __future__ import annotations

from .coordinate import Coordinate


class Region:
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        self._start: Coordinate = start
        self._end: Coordinate = end

    @property
    def start(self) -> Coordinate:
        return self._start

    @property
    def end(self) -> Coordinate:
        return self._end

    def height(self) -> float:
        return (self.end.y - self.start.y)

    def width(self) -> float:
        return (self.end.x - self.start.x)

    def __lt__(self, other: Region) -> bool:
        return (self._start < other.start)
