from os import listdir, makedirs
from os.path import basename, dirname, exists, isdir
from re import sub

from tabulate import tabulate

from src.model.data import Data
from src.utils.descending import Descending
from src.utils.instances import InstanceSet
from src.utils.order_key import OrderKey
from src.utils.split_mode import SplitMode


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


def make_ibge_table(data: list[list[str]], file: str, caption: str,
                    label: str, fonte: str = "autor", nota: str = "", legend: str = "",
                    headers: list[str] = None, tablefmt: str = "latex", ibge: bool = True
                    ) -> None:
    table = tabulate(data, tablefmt=tablefmt, headers=headers)
    lines = begin_environment(environment="table", position="!htb", caption=caption, label=label)
    tabular = file.replace("tables", "tabular")
    write_environment(tex_file=tabular, lines=table)
    if ibge:
        lines += [
            "\\IBGEtab{}{\n",
            "\\input{" + tabular[:-4] + "}\n",
            "}{}\n",
        ]
    else:
        lines.append("\\input{" + tabular[:-4] + "}\n")
    lines += end_environment(environment="table", fonte=fonte, legend=legend, nota=nota)
    write_environment(tex_file=file, lines=lines)
    return None


def data_to_ibge_table(data_file: str, tex_file: str, caption: str, label: str,
                       short: bool = True, headers: list[str] = None,
                       columns: list[int] = None, fonte: str = "", nota: str = "",
                       tablefmt: str = "latex", ibge: bool = True) -> None:
    data = get_data(data_file=data_file, columns=columns, short=short)
    make_ibge_table(data=data, file=tex_file, caption=caption, label=label,
                    fonte=fonte, nota=nota, headers=headers, tablefmt=tablefmt, ibge=ibge)
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
                                                    "Quality %", "Time (s)", "Items %"],
                                           ibge=True
                                           )
                        with open("aftertext/anexos.tex", "a") as f:
                            f.write("\\input{" + tex_file[:-4] + "}\n")

    return None


def make_figure(tex_file: str, image_file: str, caption: str, label: str,
                fonte: str = "", nota: str = "", legend: str = "",
                scale: float = 1) -> None:
    lines = begin_environment(environment="figure", position="H", caption=caption,
                              label=label, hide=True)
    lines.append(f"    \\includegraphics[scale={scale}]" + "{" + image_file + "}\n")
    lines += end_environment(environment="figure", fonte=fonte, legend=legend, nota=nota)
    write_environment(tex_file=tex_file, lines=lines)
    return None


def folder_image_to_figure(folder: str = "instances/BKW") -> None:
    folder_name = basename(dirname(f"{folder}/"))
    for file_name in sorted(listdir(folder)):
        file_name = file_name[:-6]
        for split in SplitMode:
            split = split.name
            for order in OrderKey:
                order = order.name
                for descending in [True, False]:
                    folder_with_figures = f"output/figures/{folder_name}/{file_name}/{split}" \
                                          f"/{order}/{descending}".lower()
                    if not exists(folder_with_figures):
                        continue
                    for figure_name in sorted(listdir(folder_with_figures)):
                        figure_name = figure_name[:-4]
                        figure_file = f"{folder_with_figures}/{figure_name}"
                        tex_file = f"utils/figures/{folder_name}/{file_name}/{split}" \
                                   f"/{order}/{descending}/{figure_name}.tex".lower()
                        caption = f"Estado final da instância {file_name.upper()} com " \
                                  f"configuração: Split={split}," \
                                  f"Order={order}, descending={descending}"
                        make_figure(tex_file=tex_file, image_file=figure_file, caption=caption,
                                    label=f"{file_name}-{split}-{order}-{descending}".lower(),
                                    fonte="autor", scale=0.5)
                        with open("aftertext/anexos.tex", "a") as f:
                            f.write("\\input{" + f"{tex_file[:-4]}" + "}\n")

    return None


def begin_environment(environment: str, position: str,
                      caption: str, label: str,
                      hide: bool = False) -> list[str]:
    cap = "\\caption"
    if hide:
        cap += "[]"
    cap += "{" + caption + "}"
    lines: list[str] = [
        "\\begin{" + environment + "}[" + f"{position}]\n",
        "    \\centering\n"
        "    " + f"{cap}\n",
        "    \\label{" + f"{environment[:3]}:" + label + "}\n",
    ]
    return lines


def end_environment(environment: str, fonte: str,
                    legend: str = "", nota: str = "") -> list[str]:
    lines: list[str] = []
    if legend:
        lines.append("    \\legend{" + legend + "}\n")
    if nota:
        lines.append("    \\nota{" + nota + "}\n")
    if fonte:
        lines.append("    \\fonte{" + fonte + "}\n")
    lines.append("\\end{" + environment + "}")
    return lines


def write_environment(tex_file: str, lines: list[str] | str) -> None:
    folder = dirname(tex_file)
    makedirs(folder, exist_ok=True)
    with open(tex_file, "w") as file:
        if isinstance(lines, list):
            file.writelines(lines)
        else:
            file.write(lines)
    return None


def read_file(filename: str) -> list[Data]:
    with open(filename, "r") as f:
        lines = f.readlines()

    datas: list[Data] = []
    for line in lines[2:]:
        splitted = line.split()
        name, split, order, descending, quality, time, items = splitted
        instance_set = sub(r"\d", "", name)
        data = Data(instance_name=name, instance_set=instance_set, split=split, order=order,
                    descending=descending, quality=quality, time=time, inside_items=items)
        datas.append(data)

    return datas


def filter_datas(data_set: list[Data], instance_name: str = None, instanceset: str = None,
                 splitmode: str = None, orderkey: str = None, descending: str = None
                 ) -> list[Data]:
    filtered: list[Data] = []
    for data in data_set:
        if data.filter(instance_name=instance_name, instance_set=instanceset,
                       split=splitmode, order=orderkey, descending=descending):
            filtered.append(data)
    return filtered


def data_to_data_obj(datas: list[list[str]]) -> list[Data]:
    data_set: list[Data] = []
    for data in datas:
        name, split, order, descending, quality, time, items = data
        quality = float(quality)
        time = float(time)
        items = float(items)
        instance_set = sub(r"\d", "", name)
        data = Data(instance_name=name, instance_set=instance_set, split=split, order=order,
                    descending=descending, quality=quality, time=time, inside_items=items)
        data_set.append(data)
    return data_set


def compare(data_set: list[Data], iterable,
            count_wons: bool = True, short: bool = True) -> None:
    data_set_filtered: dict[str, list[Data]] = {}
    name = iterable.__name__
    headers = [name]
    if count_wons:
        headers += ["Wons", "Draws"]
    headers += ["Quality %", "Items %", "Time (s)"]
    wons: dict[str, int] = {}
    draws: dict[str, int] = {}
    quality: dict[str, float] = {}
    items: dict[str, float] = {}
    time: dict[str, float] = {}
    for key in iterable:
        data_set_filtered[key] = eval(f"filter_datas(data_set={data_set}, "
                                      f"{name.lower()}=key.name)")
        wons[key] = 0
        draws[key] = 0
        quality[key] = 0
        items[key] = 0
        time[key] = 0

    size = len(data_set_filtered[iterable(1)])
    for idx in range(size):
        qualities = []
        for key, value in data_set_filtered.items():
            try:
                quality[key] += value[idx].quality
                items[key] += value[idx].inside_items
                time[key] += value[idx].time
                qualities.append(value[idx].quality)
            except IndexError:
                pass
        if not count_wons:
            continue
        greatest = max(qualities)
        draw: bool = qualities.count(greatest) > 1
        for key, value in data_set_filtered.items():
            try:
                if (value[idx].quality == greatest):
                    wons[key] += 1
                    if draw:
                        draws[key] += 1
            except IndexError:
                pass
    data = []
    for key in iterable:
        size = len(data_set_filtered[key])
        quality[key] /= size
        items[key] /= size
        time[key] /= size
        new_data = [key.name]
        if short:
            new_data[0] = new_data[0][0]
        if count_wons:
            new_data += [wons[key], draws[key]]
        new_data += [quality[key], items[key], time[key]]
        data.append(new_data)
    make_ibge_table(data=data, file=f"utils/tables/compare/{name.lower()}.tex",
                    caption=f"Resultado da comparação entre {name}.", label=name.lower(),
                    headers=headers)
    return None


def compare_descending(data_set: list[Data]) -> None:
    return compare(data_set=data_set, iterable=Descending)


def compare_split(data_set: list[Data]) -> None:
    return compare(data_set=data_set, iterable=SplitMode)


def compare_order(data_set: list[Data]) -> None:
    return compare(data_set=data_set, iterable=OrderKey)


def compare_instance_set(data_set: list[Data]) -> None:
    return compare(data_set=data_set, iterable=InstanceSet, count_wons=False, short=False)


def compare_combinations(data_set: list[Data]) -> None:
    data_set_filtered: dict[tuple[str, str, str], list[Data]] = {}
    headers = ["Split", "Order", "Descending", "Wons", "Draws", "Quality %", "Items %", "Time (s)"]
    wons: dict[tuple[str, str, str], int] = {}
    draws: dict[tuple[str, str, str], int] = {}
    quality: dict[tuple[str, str, str], float] = {}
    items: dict[tuple[str, str, str], float] = {}
    time: dict[tuple[str, str, str], float] = {}
    for split in SplitMode:
        split = split.name[0]
        for order in OrderKey:
            order = order.name[0]
            for descending in Descending:
                descending = descending.name[0]
                key: tuple[str, str, str] = (split, order, descending)
                data_set_filtered[key] = filter_datas(data_set=data_set, splitmode=split,
                                                      orderkey=order, descending=descending)
                wons[key] = 0
                draws[key] = 0
                quality[key] = 0
                items[key] = 0
                time[key] = 0

    size = 45  # len(data_set) / (len(SplitMode) * len(OrderKey) * len(Descending))
    for idx in range(size):
        qualities = []
        for key, value in data_set_filtered.items():
            try:
                quality[key] += value[idx].quality
                items[key] += value[idx].inside_items
                time[key] += value[idx].time
                qualities.append(value[idx].quality)
            except IndexError:
                pass
        greatest = max(qualities)
        draw: bool = qualities.count(greatest) > 1
        for key, value in data_set_filtered.items():
            try:
                if (value[idx].quality == greatest):
                    wons[key] += 1
                    if draw:
                        draws[key] += 1
            except IndexError:
                pass
    data = []
    for key in data_set_filtered.keys():
        quality[key] /= size
        items[key] /= size
        time[key] /= size
        data.append([key[0], key[1], key[2], wons[key], draws[key],
                     quality[key], items[key], time[key]])
    make_ibge_table(data=data, file=f"utils/tables/compare/combinations.tex",
                    caption=f"Resultado da comparação entre todas combinações.",
                    label="combinations", headers=headers)
    return None
