from __future__ import annotations

from .coordinate import Coordinate
from .item import Item


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

    def split_horizontally(self, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = self.end
        region0 = Region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        end = (self.end.x, item.position.y + item.height)
        region1 = Region(start=start, end=end)
        return (region0, region1)

    def split_vertically(self, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = (item.position.x + item.width, self.end.y)
        region0 = Region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        end = self.end
        region1 = Region(start=start, end=end)
        return (region0, region1)

    def fake_split(self, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = self.end
        region0 = Region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        region1 = Region(start=start, end=end)
        return (region0, region1)
