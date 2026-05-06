"""Builds a sklearn preprocessing pipeline that applies standard scaling to numeric features."""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_preprocessor() -> Pipeline:
    return Pipeline([("scaler", StandardScaler())])
