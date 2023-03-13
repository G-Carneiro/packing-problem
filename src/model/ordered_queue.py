from typing import TypeVar

T = TypeVar("T")


class OrderedQueue(list[T]):
    def __init__(self, items: list[T] = None) -> None:
        super().__init__()
        if (items is not None):
            for item in items:
                self.append(item)

    def append(self, data: T) -> None:
        for idx, item in enumerate(self):
            if (data < item):
                self.insert(idx, data)
                return None

        super().append(data)
        return None
