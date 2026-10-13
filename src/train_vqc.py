"""
QuantumShield — QFF 2026
Train the 4-qubit VQC on the ideal simulator.
"""

from pathlib import Path
import json

import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import accuracy_score

from src.problem import prepare_q3_dataset
from src.classifier import probability_class_1, predict


ROOT = Path(__file__).resolve().parents[1]

# Store optimization history for plotting later.
HISTORY = []

# Counter so we can see progress.
EVALUATION_COUNT = 0


def binary_cross_entropy(y_true, probabilities):
    """
    Binary cross-entropy classification loss.
    """

    probabilities = np.clip(
        probabilities,
        1e-8,
        1.0 - 1e-8,
    )

    loss = -np.mean(
        y_true * np.log(probabilities)
        + (1 - y_true) * np.log(1 - probabilities)
    )

    return float(loss)


def cost_function(weights, X_train, y_train):
    """
    Evaluate VQC loss across the complete training set.
    """

    global EVALUATION_COUNT

    probabilities = np.array([
        probability_class_1(sample, weights)
        for sample in X_train
    ])

    loss = binary_cross_entropy(
        y_train,
        probabilities,
    )

    predictions = (
        probabilities >= 0.5
    ).astype(int)

    accuracy = accuracy_score(
        y_train,
        predictions,
    )

    EVALUATION_COUNT += 1

    HISTORY.append({
        "evaluation": EVALUATION_COUNT,
        "loss": float(loss),
        "training_accuracy": float(accuracy),
    })

    print(
        f"Evaluation {EVALUATION_COUNT:03d} | "
        f"Loss: {loss:.6f} | "
        f"Train accuracy: {accuracy:.4f}"
    )

    return loss


def main():

    print()
    print("QuantumShield — Ideal VQC Training")
    print("=" * 55)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    print()
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Trainable weights: 8")

    # Reproducible initialization.
    rng = np.random.default_rng(42)

    initial_weights = rng.uniform(
        low=-np.pi,
        high=np.pi,
        size=8,
    )

    print()
    print("Initial weights:")
    print(np.round(initial_weights, 4))

    print()
    print("Starting optimization...")
    print("-" * 55)

    result = minimize(
        cost_function,
        initial_weights,
        args=(X_train, y_train),
        method="COBYLA",
        options={
            "maxiter": 80,
            "rhobeg": 0.5,
            "tol": 1e-4,
        },
    )

    trained_weights = result.x

    print("-" * 55)
    print()
    print("Optimization finished")
    print("---------------------")

    print(f"Success             : {result.success}")
    print(f"Optimizer message   : {result.message}")
    print(f"Final loss          : {result.fun:.6f}")
    print(f"Function evaluations: {result.nfev}")

    print()
    print("Trained weights:")
    print(np.round(trained_weights, 6))

    # ---------------------------------------------
    # Final ideal predictions
    # ---------------------------------------------

    train_predictions = np.array([
        predict(sample, trained_weights)
        for sample in X_train
    ])

    test_predictions = np.array([
        predict(sample, trained_weights)
        for sample in X_test
    ])

    train_accuracy = accuracy_score(
        y_train,
        train_predictions,
    )

    test_accuracy = accuracy_score(
        y_test,
        test_predictions,
    )

    print()
    print("Ideal classifier results")
    print("------------------------")

    print(
        f"Training accuracy : "
        f"{train_accuracy:.4f} "
        f"({train_accuracy * 100:.2f}%)"
    )

    print(
        f"Testing accuracy  : "
        f"{test_accuracy:.4f} "
        f"({test_accuracy * 100:.2f}%)"
    )

    # ---------------------------------------------
    # Save results
    # ---------------------------------------------

    results_dir = ROOT / "results"
    tables_dir = results_dir / "tables"

    tables_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    weights_path = (
        tables_dir / "trained_vqc_weights.npy"
    )

    np.save(
        weights_path,
        trained_weights,
    )

    history_path = (
        tables_dir / "training_history.json"
    )

    with open(
        history_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            HISTORY,
            file,
            indent=2,
        )

    summary = {
        "optimizer": "COBYLA",
        "seed": 42,
        "maxiter": 80,
        "training_samples": int(len(X_train)),
        "testing_samples": int(len(X_test)),
        "train_accuracy": float(train_accuracy),
        "test_accuracy": float(test_accuracy),
        "final_loss": float(result.fun),
        "function_evaluations": int(result.nfev),
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
    }

    summary_path = (
        tables_dir / "ideal_vqc_summary.json"
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
        )

    print()
    print("[OK] Trained model saved:")
    print(weights_path)

    print()
    print("[OK] Training history saved:")
    print(history_path)

    print()
    print("[OK] Ideal summary saved:")
    print(summary_path)

    print()
    print("Ideal VQC training completed.")


if __name__ == "__main__":
    main()