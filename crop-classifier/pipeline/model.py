"""Wraps RandomForestClassifier as a configurable crop classifier; swap for XGBoost by changing the estimator."""

from sklearn.ensemble import RandomForestClassifier


def build_model(hyperparams: dict):
    return RandomForestClassifier(
        n_estimators=hyperparams.get("n_estimators", 100),
        max_depth=hyperparams.get("max_depth", None),
        random_state=hyperparams.get("random_state", 42),
    )
