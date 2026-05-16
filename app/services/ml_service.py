import numpy as np
import joblib
import pandas as pd
from functools import lru_cache
from pathlib import Path

from app.schemas.crop_type import CropType
from app.schemas.crops_request import CropsRequest
from app.schemas.crops_response import CropsResponse, CropScore

_ARTIFACT_PATH = Path(__file__).parent.parent / "models" / "crop_classifier.pkl"


@lru_cache(maxsize=1)
def _load_artifact() -> dict:
    return joblib.load(_ARTIFACT_PATH)


def get_crop_recommendations(request: CropsRequest) -> CropsResponse:
    artifact = _load_artifact()
    model = artifact["model"]
    preprocessor = artifact["preprocessor"]
    label_encoder = artifact["label_encoder"]

    input_df = pd.DataFrame([{
        "temperature": request.temperature,
        "humidity": request.humidity,
        "moisture": request.moisture,
        "soil_type": request.soil_type.value,
        "nitrogen": request.nitrogen,
        "ph": request.ph,
    }])

    X_proc = preprocessor.transform(input_df)
    probabilities = model.predict_proba(X_proc)[0]

    sorted_indices = np.argsort(probabilities)[::-1]
    recommendations = [
        CropScore(crop=CropType.from_dataset_label(label_encoder.classes_[idx]), recommendation_score=round(float(probabilities[idx]), 4))
        for idx in sorted_indices
    ]

    return CropsResponse(
        best_crop=recommendations[0].crop,
        recommendations=recommendations,
    )
