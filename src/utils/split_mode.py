from enum import Enum


class SplitMode(Enum):
    VERTICALLY = "Vertical"
    HORIZONTALLY = "Horizontal"
    MAX_AREA = "Maior área"
    NONE = "Sobrepostas"
