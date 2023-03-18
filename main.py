from time import time

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from src.model.item import Item
from src.utils.order_mode import OrderMode
from src.utils.split_mode import SplitMode


def export_model(model: Item, figure_file: str) -> None:
    fig, ax = plt.subplots()
    box = Rectangle(xy=(0, 0), width=model.width, height=model.height, alpha=0.1)
    ax.add_patch(box)
    cmap = plt.cm.get_cmap('brg', len(model.items))
    for idx, item in enumerate(model.items):
        if item.position is None:
            continue
        x = item.position.x
        y = item.position.y
        rect = Rectangle(xy=(x, y), width=item.width, height=item.height,
                         facecolor=cmap(idx), alpha=0.2, linewidth=1, edgecolor='k')
        ax.add_patch(rect)
        cx = x + rect.get_width() / 2
        cy = y + rect.get_height() / 2
        ax.annotate(f"{idx}", (cx, cy), color='black', weight='bold', fontsize=10, ha='center',
                    va='center')

    plt.xlim(0, model.width)
    plt.ylim(0, model.height)
    plt.savefig(figure_file)
    plt.close()
    return None


def main() -> None:
    num_tests: int = 1
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
                    else:
                        export_model(model=box, figure_file=f"output/bkw{file_id}_"
                                                            f"{split.name.lower()}_"
                                                            f"{order.name.lower()}_"
                                                            f"{str(descending).lower()}.png")
        exit()


if __name__ == "__main__":
    main()
