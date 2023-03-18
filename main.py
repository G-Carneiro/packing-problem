from time import time

from src.model.item import Item
from src.utils.order_mode import OrderMode
from src.utils.split_mode import SplitMode


def main() -> None:
    num_tests: int = 5
    for file_id in range(1, 14):
        file = f"references/bkw/BKW{file_id}"
        with open(file, "r") as f:
            lines = f.readlines()
        for split in SplitMode:
            for order in OrderMode:
                for descending in [True, False]:
                    for _ in range(num_tests):
                        print(order, split, descending)
                        items: list[Item] = []
                        for line in lines[2:]:
                            _, width, height = line.split()
                            items.append(Item(width=float(width), height=float(height)))
                        width, height = lines[1].split()
                        box = Item(width=float(width), height=float(height), items=items)
                        start = time()
                        box.solve(order_mode=order, split_mode=split, decrescent=descending)
                        end = time() - start
                        print(box.regions)
                        for item in box.items:
                            print(item.position)
        exit()


if __name__ == "__main__":
    main()
