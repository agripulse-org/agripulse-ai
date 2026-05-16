import pandas as pd
from typing import List, Tuple

_COLUMN_MAP = {
    "Temperature": "temperature",
    "Humidity": "humidity",
    "Moisture": "moisture",
    "Soil Type": "soil_type",
    "Nitrogen": "nitrogen",
    "pH": "ph",
    "Crop Type": "crop_type",
}


def load_dataset(dataset_path: str, features: List[str]) -> Tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(dataset_path).rename(columns=_COLUMN_MAP)
    X = df[features]
    y = df["crop_type"]
    return X, y
