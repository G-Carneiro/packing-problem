from __future__ import annotations

from .coordinate import Coordinate


class Region:
    def __init__(self,
                 start: Coordinate | tuple[float, float],
                 end: Coordinate | tuple[float, float]
                 ) -> None:
        if isinstance(start, tuple):
            start = Coordinate(x=start[0], y=start[1])
        if isinstance(end, tuple):
            end = Coordinate(x=end[0], y=end[1])

        self._start: Coordinate = start
        self._end: Coordinate = end
        self._height: float = end.y - start.y
        self._width: float = end.x - start.x

    @property
    def start(self) -> Coordinate:
        return self._start

    @property
    def position(self) -> Coordinate:
        return self.start

    @property
    def end(self) -> Coordinate:
        return self._end

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def area(self) -> float:
        return (self.height * self.width)

    def __lt__(self, other: Region) -> bool:
        return (self._start < other.start)

    def __repr__(self) -> str:
        return f"{self.start} {self.end}"
