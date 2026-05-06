"""Reads the dataset CSV, trains a crop classifier model, and exports it as a .pkl file into app/models/."""

import yaml
import joblib
from pathlib import Path
from data.loader import load_dataset
from pipeline.preprocessor import build_preprocessor
from pipeline.model import build_model


def train():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    X, y = load_dataset(config["data"]["dataset_path"], config["features"])
    preprocessor = build_preprocessor()
    X_processed = preprocessor.fit_transform(X)

    model = build_model(config["hyperparams"])
    model.fit(X_processed, y)

    output_path = Path(__file__).parent.parent / "app" / "models" / "crop_classifier.pkl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "preprocessor": preprocessor}, output_path)
    print(f"Model saved to {output_path}")


if __name__ == "__main__":
    train()
