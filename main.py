from os import listdir, makedirs, scandir
from time import time

from tabulate import tabulate

from src.model.item import Item
from src.model.model import Model
from src.utils.folders import *
from src.utils.order_mode import OrderMode
from src.utils.split_mode import SplitMode


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
    num_tests: int = 5
    total_time = 0
    for idx, file_name in enumerate(sorted(listdir(folder))):
        file = f"{folder}/{file_name}"
        with open(file, "r") as f:
            lines = f.readlines()
        items: list[Item] = []
        for line in lines[2:]:
            _, width, height = line.split()
            items.append(Item(width=float(width), height=float(height)))
        width, height = lines[1].split()
        box = Item(width=float(width), height=float(height))
        for split in SplitMode:
            for order in OrderMode:
                for descending in [True, False]:
                    exec_time = 0
                    model = Model(name=file_name, instance="bkw", box=box, items=items,
                                  order=order, split=split, decrescent=descending)
                    for _ in range(num_tests):
                        print(f"[Starting] file={file_name} split={split.name} order={order.name} "
                              f"decrescent={descending}")
                        model.reset()
                        start = time()
                        model.solve()
                        exec_time += time() - start
                        total_time += exec_time
                        print(f"[Finished] file={file_name} split={split.name} order={order.name} "
                              f"decrescent={descending} exec={exec_time} total={total_time}")

                    exec_time /= num_tests
                    # model.to_csv(csv_folder=CSV, exec_time=exec_time)
                    model.export_model(folder=FIGURES, show_regions=(not idx),
                                       show_labels=(idx < 6))

    csv_to_table(csv_folder=CSV, table_folder=DATA)
    return None


if __name__ == "__main__":
    main()
