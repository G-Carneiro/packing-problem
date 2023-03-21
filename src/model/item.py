from __future__ import annotations

from os import makedirs
from typing import NoReturn

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .coordinate import Coordinate
from .ordered_queue import OrderedQueue
from .region import NotRegion, Region
from ..utils.order_mode import OrderMode
from ..utils.split_mode import SplitMode


class Item:
    id_: int = 0

    def __init__(self,
                 width: float = float("inf"),
                 height: float = float("inf"),
                 demand: int = 1,
                 copies: int = 1,
                 items: list[Item] = (),
                 ) -> None:
        self._id: int = Item.id_
        Item.id_ += 1
        self._width: float = width
        self._height: float = height
        self._demand: int = demand
        self._copies: int = copies
        self._items: list[Item] = items
        self._area: float = width * height
        self._perimeter: float = 2 * (width + height)
        self._position: Coordinate | None = None
        self._export_id: int = 0
        self._regions: OrderedQueue[Region] = OrderedQueue([Region((0, 0), (width, height))])

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
    def items(self) -> list[Item]:
        return self._items

    def sorted_items(self, order: OrderMode = OrderMode.NONE, reverse: bool = False) -> list[Item]:
        if order != OrderMode.NONE:
            return sorted(self._items, key=lambda x: eval(f"x.{order.name.lower()}"),
                          reverse=reverse)
        return self.items

    @property
    def regions(self) -> OrderedQueue[Region]:
        return self._regions

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
    def position(self, coordinate: Coordinate | None) -> NoReturn:
        self._position = coordinate

    def coords(self) -> tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
        return (self.position, self.position + (0, self.height),
                self.position + (self.width, self.height), self.position + (self.width, 0))

    def percent_free(self) -> float:
        return (100 - self.percent_busy())

    def percent_busy(self) -> float:
        busy_area: float = 0
        for item in self.items:
            if item.position is not None:
                busy_area += item.area
        return (busy_area / self.area * 100)

    def solution_quality(self) -> float:
        for item in self.items:
            if item.position is None:
                break
        else:
            return 100
        return self.percent_busy()

    def inside_items(self) -> int:
        num_items: int = 0
        for item in self.items:
            if item.position is not None:
                num_items += 1

        return num_items

    def outside_items(self) -> int:
        return (len(self.items) - self.inside_items())

    def inside_items_percent(self) -> float:
        return (self.inside_items() / len(self.items) * 100)

    def outside_item_percent(self) -> float:
        return (self.outside_items() / len(self.items) * 100)

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

    def replace_region(self, original: Region, split: tuple[Region, Region]) -> None:
        self._regions.remove(original)
        r0, r1 = split
        if r0 is not None:
            self._regions.append(r0)
        if r1 is not None:
            self._regions.append(r1)
        return None

    @staticmethod
    def new_region(start: Coordinate | tuple[float, float],
                   end: Coordinate | tuple[float, float]) -> Region | None:
        try:
            region = Region(start=start, end=end)
        except NotRegion:
            return None

        return region

    def split_horizontally(self, region: Region, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = region.end
        region0 = self.new_region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        end = (region.end.x, item.position.y + item.height)
        region1 = self.new_region(start=start, end=end)
        return (region0, region1)

    def split_vertically(self, region: Region, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = (item.position.x + item.width, region.end.y)
        region0 = self.new_region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        end = region.end
        region1 = self.new_region(start=start, end=end)
        return (region0, region1)

    def fake_split(self, region: Region, item: Item) -> tuple[Region, Region]:
        start = (item.position.x, item.position.y + item.height)
        end = region.end
        region0 = self.new_region(start=start, end=end)
        start = (item.position.x + item.width, item.position.y)
        region1 = self.new_region(start=start, end=end)
        return (region0, region1)

    def choose_best_split(self, region: Region, item: Item) -> tuple[Region, Region]:
        split_h = self.split_horizontally(region=region, item=item)
        split_v = self.split_vertically(region=region, item=item)
        regions: list[Region] = [region for region in split_h + split_v if region is not None]
        try:
            biggest = max(regions, key=lambda x: x.area)
        except ValueError:
            return split_h
        # FIXME: find best solution
        Region.id_ -= len(regions)
        if (biggest in split_h):
            return self.split_horizontally(region=region, item=item)
        return self.split_vertically(region=region, item=item)

    def solve(self, order_mode: OrderMode, split_mode: SplitMode, decrescent: bool,
              export: bool = False, export_all: bool = False, show_regions: bool = False
              ) -> float:
        items = self.sorted_items(order=order_mode, reverse=decrescent)

        if export_all:
            self.export_model(folder=f"output/figures", order=order_mode, split=split_mode,
                              decrescent=decrescent, show_regions=show_regions)

        for item in items:
            for region in self._regions:
                if (item.width > region.width) or (item.height > region.height):
                    continue

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
                        split = self.fake_split(region=region, item=item)
                    case SplitMode.HORIZONTALLY:
                        split = self.split_horizontally(region=region, item=item)
                    case SplitMode.VERTICALLY:
                        split = self.split_vertically(region=region, item=item)
                    case _:
                        split = self.choose_best_split(region=region, item=item)

                self.replace_region(original=region, split=split)
                if export_all:
                    self.export_model(folder=f"output/figures", order=order_mode, split=split_mode,
                                      decrescent=decrescent, show_regions=show_regions)
                break
        if export and not export_all:
            self.export_model(folder=f"output/figures", order=order_mode, split=split_mode,
                              decrescent=decrescent, show_regions=show_regions)
        return self.solution_quality()

    def reset(self) -> None:
        self.position = None
        self._export_id = 0
        Region.id_ = 0
        Item.id_ = 0
        self._regions = OrderedQueue([Region((0, 0), (self.width, self.height))])
        for item in self.items:
            item.reset()
        return None

    def export_model(self, folder: str, order: OrderMode, split: SplitMode, decrescent: bool,
                     show_regions: bool = False) -> None:
        folder = f"{folder}/{split.name}/{order.name}/{decrescent}".lower()
        makedirs(folder, exist_ok=True)
        num: str = "0" * (len(str(len(self.items))) - len(str(self._export_id))) \
                   + f"{self._export_id}"
        file = f"{folder}/{num}.png"
        self._export_id += 1
        fig, ax = plt.subplots()
        box = Rectangle(xy=(0, 0), width=self.width, height=self.height, alpha=0.1)
        ax.add_patch(box)
        item_cmap = plt.get_cmap('brg', len(self.items))
        self._rectangle_cmap(iterable=self.sorted_items(order=order, reverse=decrescent),
                             cmap=item_cmap, ax=ax)
        if show_regions:
            region_cmap = plt.get_cmap('hsv', 2 * len(self.items) + 1)
            self._rectangle_cmap(iterable=self.regions, cmap=region_cmap, ax=ax)
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.savefig(file)
        plt.close()
        return None

    @staticmethod
    def _rectangle_cmap(iterable, cmap, ax) -> None:
        for idx, item in enumerate(iterable):
            if item.position is None:
                continue
            x = item.position.x
            y = item.position.y
            rect = Rectangle(xy=(x, y), width=item.width, height=item.height,
                             facecolor=cmap(item.id), alpha=0.2, linewidth=1, edgecolor='k')
            ax.add_patch(rect)
            cx = x + rect.get_width() / 2
            cy = y + rect.get_height() / 2
            if isinstance(item, Item):
                label = idx
            else:
                label = f"R{item.id}"
            ax.annotate(label, (cx, cy), color='black', weight='bold', fontsize=10, ha='center',
                        va='center')
        return None
