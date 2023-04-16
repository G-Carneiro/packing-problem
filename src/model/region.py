from __future__ import annotations

from .coordinate import Coordinate
from .rect import Rect


class NotRegion(Exception):
    pass


class Region(Rect):
    id_: int = 0

    def __init__(self,
                 start: Coordinate | tuple[float, float],
                 end: Coordinate | tuple[float, float]
                 ) -> None:
        if isinstance(start, tuple):
            start = Coordinate(x=start[0], y=start[1])
        if isinstance(end, tuple):
            end = Coordinate(x=end[0], y=end[1])

        if (start.x == end.x) or (start.y == end.y):
            raise NotRegion

        start: Coordinate = start
        self._end: Coordinate = end
        height: float = end.y - start.y
        width: float = end.x - start.x
        super().__init__(width=width, height=height, position=start)
        self._id: int = Region.id_
        Region.id_ += 1

    @property
    def id(self) -> int:
        return self._id

    @property
    def start(self) -> Coordinate:
        return self.position

    @property
    def end(self) -> Coordinate:
        return self._end

    def __lt__(self, other: Region) -> bool:
        return (self.start < other.start)

    def __eq__(self, other: Region | None) -> bool:
        if other is None:
            return False
        return (self.start == other.start and self.end == other.end)

    def __repr__(self) -> str:
        return f"{self.start} {self.end}"
