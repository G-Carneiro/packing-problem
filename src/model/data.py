from dataclasses import dataclass


@dataclass()
class Data:
    instance_name: str
    instance_set: str
    split: str
    order: str
    descending: str
    quality: float
    time: float
    inside_items: float

    def filter(self, instance_name: list[str] = None, instance_set: list[str] = None,
               split: list[str] = None, order: list[str] = None, descending: list[str] = None
               ) -> bool:
        if instance_name is None:
            instance_name = [self.instance_name]
        if instance_set is None:
            instance_set = [self.instance_set]
        if split is None:
            split = [self.split]
        if order is None:
            order = [self.order]
        if descending is None:
            descending = [self.descending]
        return (self.instance_name in instance_name and self.instance_set in instance_set
                and self.split in split and self.order in order
                and self.descending in descending)

    def __str__(self) -> str:
        return f"{self.instance_name}: {self.split} {self.order} {self.descending} " \
               f"{self.quality} {self.time} {self.inside_items}"
