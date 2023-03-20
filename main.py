from os import listdir, makedirs, path, scandir
from time import time

from pandas import DataFrame
from tabulate import tabulate

from src.model.item import Item
from src.utils.order_mode import OrderMode
from src.utils.split_mode import SplitMode


def to_csv(csv_folder: str, file_name: str, box: Item, exec_time: float,
           order: OrderMode, split: SplitMode, decrescent: bool) -> None:
    data = {"Instance": [file_name],
            "SplitMode": [split.name],
            "OrderMode": [order.name],
            "Decrescent": [decrescent],
            "Exec. Time": [exec_time],
            "Solution Quality %": [box.solution_quality()],
            "Busy %": [box.percent_busy()],
            "Free %": [box.percent_free()],
            "Nº Items": [len(box.items)],
            "Inside Items": [box.inside_items()],
            "Outside Items": [box.outside_items()],
            "Inside Items %": [box.inside_items_percent()],
            "Outside Items %": [box.outside_item_percent()]}
    _to_csv(csv_folder=csv_folder, order=order, split=split, decrescent=decrescent,
            data=data)
    _to_csv(csv_folder=f"{csv_folder}/bkw/{file_name.lower()}", order=order, split=split,
            decrescent=decrescent,
            data=data)
    return None


def _to_csv(csv_folder: str, order: OrderMode, split: SplitMode, decrescent: bool,
            data) -> None:
    files = [f"order/{order.name}", f"split/{split.name}",
             f"decrescent/{decrescent}", "all"]

    makedirs(f"{csv_folder}/order", exist_ok=True)
    makedirs(f"{csv_folder}/split", exist_ok=True)
    makedirs(f"{csv_folder}/decrescent", exist_ok=True)
    for file in files:
        file = f"{csv_folder}/{file}".lower()

        with open(file, "a") as f:
            DataFrame(data).to_csv(f, index=False,
                                   header=not bool(path.getsize(file)))

    return None


def csv_to_table(csv_folder: str, table_folder: str) -> None:
    for file in scandir(csv_folder):
        file_name = file.name
        if not file.is_file():
            csv_to_table(csv_folder=f"{csv_folder}/{file_name}",
                         table_folder=f"{table_folder}/{file_name}")
            continue
        with open(file, "r") as f:
            lines = f.readlines()

        data = []
        for line in lines:
            data.append(line.split(","))

        makedirs(table_folder, exist_ok=True)

        with open(f"{table_folder}/{file_name}.dat", "w") as f:
            s = tabulate(tabular_data=data, headers="firstrow", tablefmt="plain")
            f.write(s)
    return None


def main(folder: str = "references/bkw") -> None:
    num_tests: int = 1
    csv_folder = "output/csv"
    data_folder = "output/data"
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
                    exec_time = 0
                    for _ in range(num_tests):
                        box.reset()
                        start = time()
                        box.solve(order_mode=order, split_mode=split, decrescent=descending)
                        exec_time += time() - start

                    exec_time /= num_tests
                    to_csv(csv_folder=csv_folder, file_name=file_name, box=box,
                           exec_time=exec_time, order=order, split=split, decrescent=descending)

        break
    csv_to_table(csv_folder=csv_folder, table_folder=data_folder)
    return None


if __name__ == "__main__":
    main()
