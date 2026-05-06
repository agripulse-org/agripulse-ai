"""Reads dataset.csv from disk and returns a feature matrix X and target label series y."""

import pandas as pd
from typing import List, Tuple


def load_dataset(dataset_path: str, features: List[str]) -> Tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(dataset_path)
    X = df[features]
    y = df["label"]
    return X, y
