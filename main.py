from os import listdir, path, scandir
from time import time

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pandas import DataFrame
from tabulate import tabulate

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
    plt.savefig(figure_file.lower())
    plt.close()
    return None


def to_csv(csv_file: str, data: dict[str, list[str]]) -> None:
    with open(csv_file.lower(), "a") as f:
        DataFrame(data).to_csv(f, index=False,
                               header=not bool(path.getsize(csv_file.lower())))
    return None


def csv_to_table(csv_folder: str, table_folder: str) -> None:
    for file in scandir(csv_folder):
        file_name = file.name
        if file.is_file():
            pass
        else:
            csv_to_table(csv_folder=f"{csv_folder}/{file_name}",
                         table_folder=f"{table_folder}/{file_name}")
            continue
        with open(file, "r") as f:
            lines = f.readlines()

        data = []
        for line in lines:
            data.append(line.split(","))

        with open(f"{table_folder}/{file_name}.dat", "w") as f:
            s = tabulate(tabular_data=data, headers="firstrow", tablefmt="plain")
            f.write(s)
    return None


def main(folder: str = "references/bkw") -> None:
    num_tests: int = 1
    csv_folder = "output/csv"
    data_folder = "output/data"
    figure_folder = "output/figures"
    for file_name in sorted(listdir(folder)):
        file = f"{folder}/{file_name}"
        with open(file, "r") as f:
            lines = f.readlines()
        items: list[Item] = []
        for line in lines[2:]:
            _, width, height = line.split()
            items.append(Item(width=float(width), height=float(height)))
        width, height = lines[1].split()
        box = Item(width=float(width), height=float(height), items=items)
        for split in SplitMode:
            for order in OrderMode:
                for descending in [True, False]:
                    for _ in range(num_tests):
                        box.reset()
                        start = time()
                        box.solve(order_mode=order, split_mode=split, decrescent=descending)
                        exec_time = time() - start
                        data = {"Instance": [file_name],
                                "SplitMode": [split.name],
                                "OrderMode": [order.name],
                                "Decrescent": [descending],
                                "Exec. Time": [exec_time],
                                "Solution Quality": [box.solution_quality()],
                                "Busy %": [box.percent_busy()],
                                "Free %": [box.percent_free()],
                                "Nº Items": [len(box.items)],
                                "Inside Items": [box.inside_items()],
                                "Outside Items": [box.outside_items()],
                                "Inside Items %": [box.inside_items_percent()],
                                "Outside Items %": [box.outside_item_percent()]}
                        to_csv(csv_file=f"{csv_folder}/bkw/{file_name}", data=data)
                        to_csv(csv_file=f"{csv_folder}/order/{order.name}", data=data)
                        to_csv(csv_file=f"{csv_folder}/split/{split.name}", data=data)
                        to_csv(csv_file=f"{csv_folder}/decrescent/{descending}", data=data)
                        to_csv(csv_file=f"{csv_folder}/all", data=data)

                    else:
                        export_model(model=box, figure_file=f"{figure_folder}/{file_name}_"
                                                            f"{split.name}_"
                                                            f"{order.name}_"
                                                            f"{str(descending)}.png")
        break
    csv_to_table(csv_folder=csv_folder, table_folder=data_folder)
    return None


if __name__ == "__main__":
    main()
