from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["temperature", "humidity", "moisture", "nitrogen", "ph"]
CATEGORICAL_FEATURES = ["soil_type"]


def build_preprocessor() -> Pipeline:
    column_transformer = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline([("transformer", column_transformer)])
