from os import makedirs, path

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from pandas import DataFrame

from .coordinate import Coordinate
from .item import Item
from .ordered_queue import OrderedQueue
from .region import NotRegion, Region
from ..utils.order_mode import OrderMode
from ..utils.split_mode import SplitMode


class Model:
    def __init__(self,
                 name: str,
                 instance: str,
                 box: Item,
                 items: list[Item],
                 order: OrderMode,
                 split: SplitMode,
                 decrescent: bool = True
                 ) -> None:
        self._name: str = name
        self._instance: str = instance
        self._box: Item = box
        self._items: list[Item] = items
        self._items: list[Item] = self.sorted_items(order=order, reverse=decrescent)
        self._order: OrderMode = order
        self._split: SplitMode = split
        self._decrescent: bool = decrescent
        self._export_id: int = 0
        self._regions: OrderedQueue[Region] = OrderedQueue([Region((0, 0), (box.width,
                                                                            box.height))])

    @property
    def name(self):
        return self._name

    @property
    def box(self) -> Item:
        return self._box

    @property
    def items(self) -> list[Item]:
        return self._items

    @property
    def regions(self) -> OrderedQueue[Region]:
        return self._regions

    @property
    def order(self) -> OrderMode:
        return self._order

    @property
    def split(self) -> SplitMode:
        return self._split

    @property
    def decrescent(self) -> bool:
        return self._decrescent

    def sorted_items(self, order: OrderMode = OrderMode.ID, reverse: bool = False) -> list[Item]:
        return sorted(self._items, key=lambda x: eval(f"x.{order.name.lower()}"),
                      reverse=reverse)

    def percent_free(self) -> float:
        return (100 - self.percent_busy())

    def percent_busy(self) -> float:
        busy_area: float = 0
        for item in self.items:
            if item.position is not None:
                busy_area += item.area
        return (busy_area / self.box.area * 100)

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

    def solve(self, export: bool = False, export_all: bool = False, show_regions: bool = False
              ) -> float:
        if export_all:
            self.export_model(folder=f"output/figures", show_regions=show_regions)

        for item in self.items:
            for region in self._regions:
                if (item.width > region.width) or (item.height > region.height):
                    continue

                item.position = region.start
                match self.split:
                    case SplitMode.NONE:
                        # FIXME: two equal items in same place is posible, try use OrderedSet to
                        #  solve
                        for other in self.items:
                            if (other == item):
                                break
                            if other.conflict(other=item) or item.conflict(other=other):
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
                    self.export_model(folder=f"output/figures", show_regions=show_regions)
                break
        if export and not export_all:
            self.export_model(folder=f"output/figures", show_regions=show_regions)
        return self.solution_quality()

    def reset(self, order: OrderMode = None, split: SplitMode = None,
              decrescent: bool = None) -> None:
        if order is not None:
            self._order = order
        if split is not None:
            self._split = split
        if decrescent is not None:
            self._decrescent = decrescent
        self.box.position = None
        self._export_id = 0
        Region.id_ = 0
        Item.id_ = 0
        self._regions = OrderedQueue([Region((0, 0), (self.box.width, self.box.height))])
        for item in self.items:
            item.position = None
        return None

    def export_model(self, folder: str, show_regions: bool = False,
                     show_labels: bool = False) -> None:
        folder = f"{folder}/{self._instance}/{self._name}/{self.split.name}/{self.order.name}/" \
                 f"{self.decrescent}".lower()
        makedirs(folder, exist_ok=True)
        num: str = "0" * (len(str(len(self.items))) - len(str(self._export_id))) \
                   + f"{self._export_id}"
        file = f"{folder}/{num}.png"
        self._export_id += 1
        fig, ax = plt.subplots()
        box = Rectangle(xy=(0, 0), width=self.box.width, height=self.box.height, alpha=0.1)
        ax.add_patch(box)
        item_cmap = plt.get_cmap('brg', len(self.items))
        self._rectangle_cmap(iterable=self.items, cmap=item_cmap, ax=ax, show_labels=show_labels)
        if show_regions:
            region_cmap = plt.get_cmap('hsv', 2 * len(self.items) + 1)
            self._rectangle_cmap(iterable=self.regions, cmap=region_cmap, ax=ax,
                                 show_labels=show_labels)
        plt.xlim(0, self.box.width)
        plt.ylim(0, self.box.height)
        plt.savefig(file)
        plt.close()
        return None

    @staticmethod
    def _rectangle_cmap(iterable, cmap, ax, show_labels: bool = False) -> None:
        for idx, item in enumerate(iterable):
            if item.position is None:
                continue
            x = item.position.x
            y = item.position.y
            rect = Rectangle(xy=(x, y), width=item.width, height=item.height,
                             facecolor=cmap(item.id), alpha=0.2, linewidth=1, edgecolor='k')
            ax.add_patch(rect)
            if show_labels:
                cx = x + rect.get_width() / 2
                cy = y + rect.get_height() / 2
                if isinstance(item, Item):
                    label = idx
                else:
                    label = f"R{item.id}"
                ax.annotate(label, (cx, cy), color='black', weight='bold', fontsize=10, ha='center',
                            va='center')
        return None

    def to_csv(self, csv_folder: str, exec_time: float) -> None:
        data = {"Instance": [self._name],
                "SplitMode": [self.split.name],
                "OrderMode": [self.order.name],
                "Decrescent": [self.decrescent],
                "Exec. Time": [exec_time],
                "Solution Quality %": [self.solution_quality()],
                "Occupied %": [self.percent_busy()],
                "Free %": [self.percent_free()],
                "Nº Items": [len(self.items)],
                "Inside Items": [self.inside_items()],
                "Outside Items": [self.outside_items()],
                "Inside Items %": [self.inside_items_percent()],
                "Outside Items %": [self.outside_item_percent()]}
        self._to_csv(csv_folder=csv_folder, data=data)
        self._to_csv(csv_folder=f"{csv_folder}/bkw", data=data)
        self._to_csv(csv_folder=f"{csv_folder}/bkw/{self.name.lower()}", data=data)
        return None

    def _to_csv(self, csv_folder: str, data) -> None:
        files = [f"order/{self.order.name}", f"split/{self.split.name}",
                 f"decrescent/{self.decrescent}", "all"]

        makedirs(f"{csv_folder}/order", exist_ok=True)
        makedirs(f"{csv_folder}/split", exist_ok=True)
        makedirs(f"{csv_folder}/decrescent", exist_ok=True)
        for file in files:
            file = f"{csv_folder}/{file}".lower()

            with open(file, "a") as f:
                DataFrame(data).to_csv(f, index=False,
                                       header=not bool(path.getsize(file)))

        return None
