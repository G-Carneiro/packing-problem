from os import listdir
from os.path import basename, dirname
from time import time

from numpy import mean, median, std

from src.model.item import Item
from src.model.model import Model
from src.utils.folders import *
from src.utils.functions import *
from src.utils.order_key import OrderKey
from src.utils.split_mode import SplitMode


def main(folder: str = INSTANCES) -> None:
    num_tests: int = 5
    total_time = 0
    folder_name = basename(dirname(f"{folder}/"))
    for file_name in [sorted(listdir(folder))[-1]]:
        file = f"{folder}/{file_name}"
        file_name = file_name.split(".")[0]
        with open(file, "r") as f:
            lines = f.readlines()
        items: list[Item] = []
        for line in lines[2:]:
            _, width, height, demand, copies, profit = line.split()
            for _ in range(int(copies)):
                items.append(Item(width=float(width), height=float(height)))
        width, height = lines[1].split()
        box = Item(width=float(width), height=float(height))
        for split in SplitMode:
            for order in OrderKey:
                for descending in [True, False]:
                    exec_time = []
                    model = Model(name=file_name, instance=folder_name, box=box, items=items,
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
                              f"decrescent={descending} exec={exec_time[-1]} total={total_time}")

                    media = mean(exec_time)
                    mediana = median(exec_time)
                    desvio = std(exec_time)
                    model.to_csv(csv_folder=CSV, exec_time=media, median=mediana, std=desvio)
                    model.export_model(folder=FIGURES, show_regions=False,
                                       show_labels=False)

    csv_to_table(csv_folder=CSV, table_folder=DATA)
    return None


if __name__ == "__main__":
    main()
