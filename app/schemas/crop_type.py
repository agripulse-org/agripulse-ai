from enum import Enum


class CropType(str, Enum):
    WHEAT = "wheat"
    BARLEY = "barley"
    RYE = "rye"
    OATS = "oats"
    CORN = "corn"
    RAPESEED = "rapeseed"
    SUNFLOWER = "sunflower"
    SOYBEAN = "soybean"
    POTATO = "potato"
    SUGAR_BEET = "sugar_beet"
    TOMATO = "tomato"
    CHERRY = "cherry"
    PEACH = "peach"

    @classmethod
    def from_dataset_label(cls, label: str) -> "CropType | None":
        try:
            return cls(label.lower().replace(" ", "_"))
        except ValueError:
            return None
