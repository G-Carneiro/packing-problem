from os import makedirs, scandir

from tabulate import tabulate


def tabulate_ins2d(folder: str = "instances/GCUT"):
    for file in scandir(folder):
        with open(file, "r") as f:
            lines = f.readlines()

        data = [lines[0].split(), lines[1].split()]
        for line in lines[2:]:
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
