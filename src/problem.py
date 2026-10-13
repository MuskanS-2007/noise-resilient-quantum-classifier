"""
QuantumShield — QFF 2026
PS-Q3: Noise-Resilient Classification & Error Mitigation

Problem/data preparation utilities.
"""

from pathlib import Path

import pandas as pd

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


ROOT = Path(__file__).resolve().parents[1]


def generate_q3_dataset():
    """
    Generate the official self-contained synthetic QML dataset.

    QFF Phase 1 Master Guide:
    - 200 samples
    - 4 features
    - 3 informative features
    - binary classification
    - random_state = 42
    - 80/20 train/test split
    """

    X, y = make_classification(
        n_samples=200,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        n_classes=2,
        random_state=42,
    )

    return X, y


def prepare_q3_dataset():
    """
    Generate, split and scale the Q3 dataset.

    Scaling to [0, pi] makes each feature directly suitable
    for angle encoding in the quantum circuit.
    """

    X, y = generate_q3_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    scaler = MinMaxScaler(
        feature_range=(0, 3.141592653589793)
    )

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler,
    )


def save_dataset():
    """
    Save generated data so the experiment is transparent
    and reproducible.
    """

    X, y = generate_q3_dataset()

    raw_dir = ROOT / "data" / "raw"
    processed_dir = ROOT / "data" / "processed"

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_df = pd.DataFrame(
        X,
        columns=[
            "feature_0",
            "feature_1",
            "feature_2",
            "feature_3",
        ],
    )

    raw_df["label"] = y

    raw_path = raw_dir / "q3_synthetic_dataset.csv"
    raw_df.to_csv(raw_path, index=False)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        _,
    ) = prepare_q3_dataset()

    train_df = pd.DataFrame(
        X_train,
        columns=[
            "feature_0",
            "feature_1",
            "feature_2",
            "feature_3",
        ],
    )
    train_df["label"] = y_train

    test_df = pd.DataFrame(
        X_test,
        columns=[
            "feature_0",
            "feature_1",
            "feature_2",
            "feature_3",
        ],
    )
    test_df["label"] = y_test

    train_path = processed_dir / "q3_train.csv"
    test_path = processed_dir / "q3_test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    return raw_path, train_path, test_path