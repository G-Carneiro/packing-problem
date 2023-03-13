from __future__ import annotations

from .coordinate import Coordinate
from .ordered_queue import OrderedQueue
from .region import Region


class Item:
    def __init__(self,
                 width: float = float("inf"),
                 height: float = float("inf"),
                 demand: int = 1,
                 copies: int = 1,
                 items: set[Item] = None,
                 ) -> None:
        self._width: float = width
        self._height: float = height
        self._demand: int = demand
        self._copies: int = copies
        self._items: set[Item] = items
        self._regions: OrderedQueue[Region] = OrderedQueue([Region((0, 0), (width, height))])

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @property
    def demand(self) -> float:
        return self._demand

    @property
    def copies(self) -> int:
        return self._copies

    def solve(self) -> None:
        for item in self._items:
            for coord in sorted(self._available_pos):
                new_x: float = coord.x + item.width
                new_y: float = coord.y + item.height
                if (new_x <= self.width) and (new_y <= self.height):
                    break
