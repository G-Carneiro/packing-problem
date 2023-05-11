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

    def filter(self, instance_name: str = None, split: str = None,
               order: str = None, descending: str = None) -> bool:
        if instance_name is None:
            instance_name = self.instance_name
        if split is None:
            split = self.split
        if order is None:
            order = self.order
        if descending is None:
            descending = self.descending
        return (self.instance_name == instance_name and self.split == split
                and self.order == order and self.descending == descending)

    def __str__(self) -> str:
        return f"{self.instance_name}: {self.split} {self.order} {self.descending} " \
               f"{self.quality} {self.time} {self.inside_items}"
