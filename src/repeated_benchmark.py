"""
QuantumShield — QFF 2026
Repeated-seed robustness benchmark.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from qiskit_aer import AerSimulator

from src.problem import prepare_q3_dataset
from src.classifier import probability_class_1
from src.benchmark_noise import noisy_predict
from src.mitigation import mitigate_readout_probability
from src.noise import build_noise_model


ROOT = Path(__file__).resolve().parents[1]

SEEDS = [42, 123, 256, 512, 1024]


def main():

    print()
    print("QuantumShield — Repeated-Seed Robustness Benchmark")
    print("=" * 68)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    weights = np.load(
        ROOT
        / "results"
        / "tables"
        / "trained_vqc_weights.npy"
    )

    ideal_probabilities = np.array([
        probability_class_1(sample, weights)
        for sample in X_test
    ])

    noise_model = build_noise_model()

    simulator = AerSimulator(
        noise_model=noise_model
    )

    rows = []

    for processor in ["A", "B"]:

        print()
        print("=" * 68)
        print(f"PROCESSOR {processor}")
        print("=" * 68)

        for seed in SEEDS:

            noisy_predictions = []
            noisy_probabilities = []

            for sample in X_test:

                prediction, probability = noisy_predict(
                    sample,
                    weights,
                    processor,
                    simulator,
                    simulator_seed=seed,
                )

                noisy_predictions.append(
                    prediction
                )

                noisy_probabilities.append(
                    probability
                )

            noisy_probabilities = np.asarray(
                noisy_probabilities
            )

            mitigated_probabilities = np.array([
                mitigate_readout_probability(p)
                for p in noisy_probabilities
            ])

            mitigated_predictions = (
                mitigated_probabilities >= 0.5
            ).astype(int)

            noisy_accuracy = accuracy_score(
                y_test,
                noisy_predictions,
            )

            mitigated_accuracy = accuracy_score(
                y_test,
                mitigated_predictions,
            )

            noisy_mae = np.mean(
                np.abs(
                    noisy_probabilities
                    - ideal_probabilities
                )
            )

            mitigated_mae = np.mean(
                np.abs(
                    mitigated_probabilities
                    - ideal_probabilities
                )
            )

            print(
                f"Seed {seed:4d} | "
                f"Noisy acc: {noisy_accuracy:.4f} | "
                f"Mitigated acc: {mitigated_accuracy:.4f} | "
                f"Noisy MAE: {noisy_mae:.6f} | "
                f"Mitigated MAE: {mitigated_mae:.6f}"
            )

            rows.append({
                "processor": processor,
                "seed": seed,
                "noisy_accuracy": float(
                    noisy_accuracy
                ),
                "mitigated_accuracy": float(
                    mitigated_accuracy
                ),
                "noisy_mae": float(
                    noisy_mae
                ),
                "mitigated_mae": float(
                    mitigated_mae
                ),
            })

    dataframe = pd.DataFrame(rows)

    output_dir = (
        ROOT
        / "results"
        / "tables"
    )

    raw_path = (
        output_dir
        / "repeated_seed_results.csv"
    )

    dataframe.to_csv(
        raw_path,
        index=False,
    )

    summary = (
        dataframe
        .groupby("processor")
        .agg(
            noisy_accuracy_mean=(
                "noisy_accuracy",
                "mean",
            ),
            noisy_accuracy_std=(
                "noisy_accuracy",
                "std",
            ),
            mitigated_accuracy_mean=(
                "mitigated_accuracy",
                "mean",
            ),
            mitigated_accuracy_std=(
                "mitigated_accuracy",
                "std",
            ),
            noisy_mae_mean=(
                "noisy_mae",
                "mean",
            ),
            noisy_mae_std=(
                "noisy_mae",
                "std",
            ),
            mitigated_mae_mean=(
                "mitigated_mae",
                "mean",
            ),
            mitigated_mae_std=(
                "mitigated_mae",
                "std",
            ),
        )
        .reset_index()
    )

    summary_path = (
        output_dir
        / "repeated_seed_summary.csv"
    )

    summary.to_csv(
        summary_path,
        index=False,
    )

    print()
    print("=" * 68)
    print("FINAL REPEATED-SEED SUMMARY")
    print("=" * 68)
    print()

    print(
        summary.to_string(
            index=False
        )
    )

    print()
    print(
        f"[OK] Raw results saved: {raw_path}"
    )

    print(
        f"[OK] Summary saved: {summary_path}"
    )

    print()
    print(
        "Repeated-seed robustness benchmark completed."
    )


if __name__ == "__main__":
    main()