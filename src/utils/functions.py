from tabulate import tabulate

complete_headers = ["Instance", "SplitMode", "OrderMode", "Decrescent", "Solution Quality %",
                    "Exec. Time", "Median", "Standard deviation", "Occupied %", "Free %",
                    "Nº Items", "Inside Items", "Outside Items", "Inside Items %",
                    "Outside Items %"]


def get_data(data_file: str, columns: list[int], short: bool = True) -> list[list[str]]:
    with open(data_file, "r") as f:
        lines = f.readlines()

    data = []
    for line in lines[2:]:
        split = line.split()
        row = []
        for idx in columns:
            dat = split[idx]
            if short and (1 <= idx <= 3):
                dat = dat[0]
            row.append(dat)
        data.append(row)

    return data


def data_to_tex_table(data_file: str, tex_file: str, short: bool = True,
                      headers: list[str] = None, columns: list[int] = None
                      ) -> None:
    data = get_data(data_file=data_file, short=short, columns=columns)
    with open(tex_file, "w") as f:
        f.write(tabulate(data, tablefmt="latex_longtable", headers=headers))

    return None
