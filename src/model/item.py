from __future__ import annotations

from typing import NoReturn

from .coordinate import Coordinate


class Item:
    id_: int = 0

    def __init__(self,
                 width: float = float("inf"),
                 height: float = float("inf"),
                 ) -> None:
        self._id: int = Item.id_
        Item.id_ += 1
        self._width: float = width
        self._height: float = height
        self._area: float = width * height
        self._perimeter: float = 2 * (width + height)
        self._position: Coordinate | None = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @property
    def area(self) -> float:
        return self._area

    @property
    def perimeter(self) -> float:
        return self._perimeter

    @property
    def position(self) -> Coordinate | None:
        return self._position

    @position.setter
    def position(self, coordinate: Coordinate | None) -> NoReturn:
        self._position = coordinate

    def coords(self) -> tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
        return (self.position, self.position + (0, self.height),
                self.position + (self.width, self.height), self.position + (self.width, 0))

    def conflict(self, other: Item) -> bool:
        # adaptation of cohen-sutherland clipping algorithm
        def region_code(point: Coordinate) -> int:
            code: str = ""
            code += f"{int(point.y >= self.position.y + self.height)}"  # 1000 top
            code += f"{int(point.y <= self.position.y)}"  # 0100 bottom
            code += f"{int(point.x >= self.position.x + self.width)}"  # 0010 right
            code += f"{int(point.x <= self.position.x)}"  # 0001 left
            return int(code, 2)

        if (other.position is None) or (self.position is None):
            return False

        coords = other.coords()
        for idx, coord in enumerate(coords):
            if region_code(point=coord) & region_code(coords[idx - 1]) == 0:
                return True
        return False
