from ..utils.order_key import OrderKey


class OrderMode:
    def __init__(self, key: OrderKey, reverse: bool = True) -> None:
        self._key: OrderKey = key
        self._reverse: bool = reverse

    @property
    def key(self) -> OrderKey:
        return self._key

    @property
    def reverse(self) -> bool:
        return self._reverse

    @property
    def name(self) -> str:
        return self.key.name
