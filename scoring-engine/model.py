"""
Example ML model wrapper using scikit-learn.
This is a minimal example to demonstrate training and inference.
In production, replace with a well-audited pipeline with versioning and tests.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
from typing import List

MODEL_PATH = "scoring-engine/models/sample_rf.joblib"


def train_example_model(X: pd.DataFrame, y: pd.Series, save_path: str = MODEL_PATH):
    """
    Train a simple classifier that predicts default risk (binary) from features.
    - X: DataFrame with normalized features (columns correspond to features)
    - y: Series with 0/1 default labels
    Save pipeline to disk and return it.
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, save_path)
    return pipeline


def load_model(path: str = MODEL_PATH):
    return joblib.load(path)


def predict_proba(model, X: pd.DataFrame) -> List[float]:
    """
    Return probability of positive class (e.g., default). Convert to risk / score as needed.
    """
    probs = model.predict_proba(X)
    # assume class 1 = default risk; return probability of class 0 (goodness)
    goodness = probs[:, 0].tolist()
    return goodness
