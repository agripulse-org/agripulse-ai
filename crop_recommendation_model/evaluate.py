import yaml
import joblib
from pathlib import Path
from data.loader import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def evaluate():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    dataset_path = config_path.parent / config["data"]["dataset_path"]
    X, y_raw = load_dataset(str(dataset_path), config["features"])

    artifact_path = Path(__file__).parent.parent / "app" / "models" / "crop_classifier.pkl"
    artifact = joblib.load(artifact_path)

    label_encoder = artifact["label_encoder"]
    y = label_encoder.transform(y_raw)

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_test_processed = artifact["preprocessor"].transform(X_test)
    y_pred = artifact["model"].predict(X_test_processed)
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


if __name__ == "__main__":
    evaluate()
