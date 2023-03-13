from __future__ import annotations

from .coordinate import Coordinate


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
        self._available_pos: list[Coordinate] = [Coordinate(x=0, y=0)]

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
                    self._available_pos.remove(coord)
                    self._available_pos.append(Coordinate(new_x, coord.y))
                    self._available_pos.append(Coordinate(coord.x, new_y))
                    break
