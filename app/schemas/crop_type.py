from enum import Enum


class CropType(str, Enum):
    MAIZE = "maize"
    SUGARCANE = "sugarcane"
    COTTON = "cotton"
    TOBACCO = "tobacco"
    PADDY = "paddy"
    BARLEY = "barley"
    WHEAT = "wheat"
    MILLETS = "millets"
    OIL_SEEDS = "oil_seeds"
    PULSES = "pulses"
    GROUND_NUTS = "ground_nuts"

    @classmethod
    def from_dataset_label(cls, label: str) -> "CropType | None":
        try:
            return cls(label.lower().replace(" ", "_"))
        except ValueError:
            return None