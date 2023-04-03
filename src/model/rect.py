from typing import NoReturn

from .coordinate import Coordinate


class Rect:
    def __init__(self,
                 width: float = float("inf"),
                 height: float = float("inf"),
                 position: Coordinate | None = None
                 ) -> None:
        self._width: float = width
        self._height: float = height
        self._area: float = width * height
        self._perimeter: float = 2 * (width + height)
        self._position: Coordinate | None = position

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

    @property
    def end(self) -> Coordinate | None:
        if self.position is None:
            return None
        return self.position + (self.width, self.height)
