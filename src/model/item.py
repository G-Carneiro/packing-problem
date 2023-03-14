from __future__ import annotations

from .coordinate import Coordinate
from .ordered_queue import OrderedQueue
from .region import Region
from ..utils.order_mode import OrderMode
from ..utils.split_mode import SplitMode


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
        self._area: float = width * height
        self._perimeter: float = 2 * (width + height)
        self._position: Coordinate | None = None
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
    def position(self, coordinate: Coordinate | None) -> None:
        self._position = coordinate

    def conflict(self, other: Item) -> bool:
        if (other.position is None):
            return False
        if (self.position.x):  # cohen-... CG
            pass

        return False

    def replace_region(self, original: Region, split: tuple[Region, Region]) -> None:
        self._regions.remove(original)
        self._regions.append(split[0])
        self._regions.append(split[1])
        return None

    def solve(self, order_mode: OrderMode, split_mode: SplitMode, decrescent: bool) -> None:
        match order_mode:
            case OrderMode.AREA:
                items: list[Item] = sorted(self._items, key=lambda x: x.area, reverse=decrescent)
            case OrderMode.HEIGHT:
                items: list[Item] = sorted(self._items, key=lambda x: x.height, reverse=decrescent)
            case OrderMode.WIDTH:
                items: list[Item] = sorted(self._items, key=lambda x: x.width, reverse=decrescent)
            case OrderMode.PERIMETER:
                items: list[Item] = sorted(self._items, key=lambda x: x.perimeter,
                                           reverse=decrescent)
            case _:
                items = list(self._items)

        for item in items:
            for region in self._regions:
                if (item.width <= region.width) and (item.height <= region.height):
                    item.position = region.start

                match split_mode:
                    case SplitMode.NONE:
                        for other in items:
                            if (other == item):
                                break
                            if item.conflict(other=other):
                                item.position = None
                                break

                        if (item.position is None):
                            continue
                        split = region.fake_split(item=item)
                    case SplitMode.HORIZONTALLY:
                        split = region.split_horizontally(item=item)
                    case SplitMode.VERTICALLY:
                        split = region.split_vertically(item=item)
                    case _:
                        split_h = region.split_horizontally(item=item)
                        split_v = region.split_vertically(item=item)
                        biggest = max(split_h[0], split_h[1], split_v[0], split_v[1])
                        if (biggest in split_h):
                            split = split_h
                        else:
                            split = split_v

                self.replace_region(original=region, split=split)
                break
