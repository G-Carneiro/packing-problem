from typing import TypeVar

T = TypeVar("T")


class OrderedQueue(list[T]):
    def __init__(self, items: list[T] = None) -> None:
        super().__init__()
        if (items is not None):
            for item in items:
                self.append(item)

    def append(self, data: T) -> None:
        lim_inf: int = 0
        lim_sup: int = len(self) - 1
        while (lim_inf <= lim_sup):
            idx: int = (lim_sup + lim_inf) // 2
            if (data == self[idx]):
                break
            elif (data > self[idx]):
                lim_inf = idx + 1
            else:
                lim_sup = idx - 1
        else:
            self.insert(lim_inf, data)

        # for idx, item in enumerate(self):
        #     if (data < item):
        #         self.insert(idx, data)
        #         return None

        # super().append(data)
        return None
