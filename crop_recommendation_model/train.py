import yaml
import joblib
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

from data.loader import load_dataset
from pipeline.preprocessor import build_preprocessor

CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def _tune_random_forest(X, y):
    param_dist = {
        "n_estimators": [200, 300, 400, 500],
        "max_depth": [None, 15, 20, 30],
        "max_features": ["sqrt", "log2", 0.3, 0.5],
        "min_samples_leaf": [1, 2, 4],
        "min_samples_split": [2, 5, 10],
    }
    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=42),
        param_dist, n_iter=20, cv=CV,
        scoring="accuracy", n_jobs=-1, random_state=42, verbose=0,
    )
    search.fit(X, y)
    print(f"  RandomForest best CV accuracy: {search.best_score_:.4f}  params: {search.best_params_}")
    return search.best_estimator_


def _tune_xgboost(X, y, n_classes):
    param_dist = {
        "n_estimators": [200, 300, 400],
        "max_depth": [4, 6, 8, 10],
        "learning_rate": [0.05, 0.1, 0.15, 0.2],
        "subsample": [0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.6, 0.7, 0.8, 1.0],
        "min_child_weight": [1, 3, 5],
    }
    search = RandomizedSearchCV(
        XGBClassifier(
            objective="multi:softprob",
            num_class=n_classes,
            eval_metric="mlogloss",
            verbosity=0,
            random_state=42,
        ),
        param_dist, n_iter=20, cv=CV,
        scoring="accuracy", n_jobs=-1, random_state=42, verbose=0,
    )
    search.fit(X, y)
    print(f"  XGBoost best CV accuracy: {search.best_score_:.4f}  params: {search.best_params_}")
    return search.best_estimator_


def _tune_gradient_boosting(X, y):
    param_dist = {
        "n_estimators": [200, 300, 400],
        "max_depth": [3, 4, 5],
        "learning_rate": [0.05, 0.1, 0.15],
        "subsample": [0.7, 0.8, 0.9],
        "max_features": ["sqrt", "log2", 0.5],
    }
    search = RandomizedSearchCV(
        GradientBoostingClassifier(random_state=42),
        param_dist, n_iter=15, cv=CV,
        scoring="accuracy", n_jobs=-1, random_state=42, verbose=0,
    )
    search.fit(X, y)
    print(f"  GradientBoosting best CV accuracy: {search.best_score_:.4f}  params: {search.best_params_}")
    return search.best_estimator_


def train():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    dataset_path = config_path.parent / config["data"]["dataset_path"]
    X, y_raw = load_dataset(str(dataset_path), config["features"])

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    n_classes = len(label_encoder.classes_)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    print("Tuning models (this may take a minute)...")
    rf = _tune_random_forest(X_train_proc, y_train)
    xgb = _tune_xgboost(X_train_proc, y_train, n_classes)
    gb = _tune_gradient_boosting(X_train_proc, y_train)

    # Soft-voting ensemble of all three tuned models
    ensemble = VotingClassifier(
        estimators=[("rf", rf), ("xgb", xgb), ("gb", gb)],
        voting="soft",
        n_jobs=-1,
    )
    ensemble.fit(X_train_proc, y_train)

    candidates = {
        "RandomForest": rf,
        "XGBoost": xgb,
        "GradientBoosting": gb,
        "Ensemble": ensemble,
    }

    results = {}
    for name, model in candidates.items():
        y_pred = model.predict(X_test_proc)
        acc = accuracy_score(y_test, y_pred)
        results[name] = {"model": model, "accuracy": acc}

        print(f"\n{'='*50}")
        print(f"Model: {name}  |  Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
        print("Confusion matrix:")
        print(confusion_matrix(y_test, y_pred))

    best_name = max(results, key=lambda n: results[n]["accuracy"])
    best_model = results[best_name]["model"]
    print(f"\nBest model: {best_name} (accuracy={results[best_name]['accuracy']:.4f})")

    output_path = Path(__file__).parent.parent / "app" / "models" / "crop_classifier.pkl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best_model,
            "preprocessor": preprocessor,
            "label_encoder": label_encoder,
        },
        output_path,
    )
    print(f"Artifact saved to {output_path}")
    print(f"Crop classes: {list(label_encoder.classes_)}")


if __name__ == "__main__":
    train()
