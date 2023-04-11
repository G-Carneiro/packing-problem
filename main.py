from os import listdir, makedirs, scandir
from time import time

from numpy import mean, median, std
from tabulate import tabulate

from src.model.item import Item
from src.model.model import Model
from src.utils.folders import *
from src.utils.order_key import OrderKey
from src.utils.split_mode import SplitMode


def to_ins2d(folder: str = "instances/OKP"):
    for file in scandir(folder):
        with open(file, "r") as f:
            lines = f.readlines()

        data = []
        for line in lines:
            new_line = line.split()
            data.append(new_line)

        with open(file, "w") as f:
            s = tabulate(tabular_data=data, tablefmt="plain")
            f.write(s)
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


def main(folder: str = INSTANCES) -> None:
    num_tests: int = 5
    total_time = 0
    for idx, file_name in enumerate(sorted(listdir(folder))[:10]):
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
            for order in OrderKey:
                for descending in [True, False]:
                    exec_time = []
                    model = Model(name=file_name, instance="bkw", box=box, items=items,
                                  order=order, split=split, decrescent=descending)
                    for _ in range(num_tests):
                        print(f"[Starting] file={file_name} split={split.name} order={order.name} "
                              f"decrescent={descending}")
                        model.reset()
                        start = time()
                        model.solve()
                        exec_time.append(time() - start)
                        total_time += exec_time[-1]
                        print(f"[Finished] file={file_name} split={split.name} order={order.name} "
                              f"decrescent={descending} exec={exec_time} total={total_time}")

                    media = mean(exec_time)
                    mediana = median(exec_time)
                    desvio = std(exec_time)
                    model.to_csv(csv_folder=CSV, exec_time=media, median=mediana, std=desvio)
                    model.export_model(folder=FIGURES, show_regions=False,
                                       show_labels=False)

    csv_to_table(csv_folder=CSV, table_folder=DATA)
    return None


def test():
    from src.model.ordered_queue import OrderedQueue
    from random import randint
    lista = []
    for _ in range(100):
        lista.append(randint(0, 100))
    print(lista)
    queue = OrderedQueue(lista)
    print(queue)


# TODO: mediana, desvio padrão - numpy
if __name__ == "__main__":
    to_ins2d()
