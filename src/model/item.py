from __future__ import annotations

from .coordinate import Coordinate
from .rect import Rect


class Item(Rect):
    id_: int = 0

    def __init__(self,
                 width: float = float("inf"),
                 height: float = float("inf"),
                 ) -> None:
        super().__init__(width=width, height=height)
        self._id: int = Item.id_
        Item.id_ += 1

    @property
    def id(self) -> int:
        return self._id

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
        elif (self.position == other.position) or (self.end == other.end):
            return True

        coords = other.coords()
        for idx, coord in enumerate(coords):
            if region_code(point=coord) & region_code(coords[idx - 1]) == 0:
                return True
        return False
