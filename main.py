from src.model.item import Item
from src.utils.order_mode import OrderMode
from src.utils.split_mode import SplitMode


def main() -> None:
    file = "references/bkw/BKW1"
    with open(file, "r") as f:
        lines = f.readlines()

    for order in OrderMode:
        for split in SplitMode:
            for descending in [True, False]:
                print(order, split, descending)
                items: set[Item] = set()
                for line in lines[2:]:
                    _, width, height = line.split()
                    items.add(Item(width=float(width), height=float(height)))
                width, height = lines[1].split()
                box = Item(width=float(width), height=float(height), items=items)
                box.solve(order_mode=order, split_mode=split, decrescent=descending)
                print(box._regions)
                for item in items:
                    print(item.position)


if __name__ == "__main__":
    main()
