from os import listdir, makedirs
from os.path import dirname, exists, isdir

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


def make_ibge_table(data: list[list[str]], file: str, caption: str,
                    label: str, fonte: str = "", nota: str = "",
                    headers: list[str] = None
                    ) -> None:
    table = tabulate(data, tablefmt="latex", headers=headers)
    lines = [
        "\\begin{table}[htb!] \n",
        "\\IBGEtab{ \n",
        "    \\caption{" + f"{caption}" + "} \n",
        "    \\label{tab:" + f"{label}" + "} \n",
        "}{ \n",
        f"{table} \n",
        "}{ \n",
    ]
    if fonte:
        lines.append("    \\fonte{" + f"{fonte}" + "} \n")
    if nota:
        lines.append("    \\nota{" + f"{nota}" + "} \n")
    lines += [
        "} \n",
        "\\end{table} \n"
    ]
    with open(file, "w") as f:
        f.writelines(lines)
    return None


def data_to_ibge_table(data_file: str, tex_file: str, caption: str, label: str,
                       short: bool = True, headers: list[str] = None,
                       columns: list[int] = None, fonte: str = "", nota: str = ""
                       ) -> None:
    data = get_data(data_file=data_file, columns=columns, short=short)
    folder = dirname(tex_file)
    makedirs(folder, exist_ok=True)
    make_ibge_table(data=data, file=tex_file, caption=caption, label=label,
                    fonte=fonte, nota=nota, headers=headers)
    return None


def folder_data_to_ibge_table(folder: str) -> None:
    for folder_name in sorted(listdir(folder)):
        dir_ = f"{folder}/{folder_name}"
        if isdir(dir_):
            for instance in sorted(listdir(dir_)):
                file = f"{dir_}/{instance}"
                if isdir(file):
                    data_file = f"{folder}/{folder_name}/{instance}/all.dat"
                    if exists(data_file):
                        tex_file = f"utils/tables/{folder_name}/{instance}.tex"
                        data_to_ibge_table(data_file=data_file,
                                           tex_file=tex_file,
                                           caption=f"Resultados da instância {instance.upper()}.",
                                           label=instance,
                                           fonte="autor",
                                           columns=[0, 1, 2, 3, 4, 5, 13],
                                           headers=["Instance", "Split", "Order", "Descending",
                                                    "Quality %", "Time (s)", "Items %"])
                        with open("aftertext/anexos.tex", "a") as f:
                            f.write("\\input{" + f"{tex_file[:-4]}" + "} \n")

    return None
