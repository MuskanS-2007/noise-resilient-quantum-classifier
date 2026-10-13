"""
QuantumShield — QFF 2026
Probability-level analysis of readout error mitigation.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.problem import prepare_q3_dataset
from src.classifier import probability_class_1


ROOT = Path(__file__).resolve().parents[1]


def main():

    print()
    print("QuantumShield — Mitigation Quality Analysis")
    print("=" * 65)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    weights_path = (
        ROOT
        / "results"
        / "tables"
        / "trained_vqc_weights.npy"
    )

    predictions_path = (
        ROOT
        / "results"
        / "tables"
        / "mitigated_predictions.csv"
    )

    weights = np.load(weights_path)

    dataframe = pd.read_csv(
        predictions_path
    )

    # Exact ideal statevector probabilities.
    ideal_probabilities = np.array([
        probability_class_1(
            sample,
            weights,
        )
        for sample in X_test
    ])

    summary = []

    for processor in ["A", "B"]:

        subset = dataframe[
            dataframe["processor"] == processor
        ].copy()

        noisy = subset[
            "probability_class_1"
        ].to_numpy()

        mitigated = subset[
            "mitigated_probability_class_1"
        ].to_numpy()

        noisy_errors = (
            noisy - ideal_probabilities
        )

        mitigated_errors = (
            mitigated - ideal_probabilities
        )

        noisy_mae = np.mean(
            np.abs(noisy_errors)
        )

        mitigated_mae = np.mean(
            np.abs(mitigated_errors)
        )

        noisy_rmse = np.sqrt(
            np.mean(noisy_errors ** 2)
        )

        mitigated_rmse = np.sqrt(
            np.mean(mitigated_errors ** 2)
        )

        mae_improvement = (
            noisy_mae - mitigated_mae
        )

        rmse_improvement = (
            noisy_rmse - mitigated_rmse
        )

        print()
        print("=" * 65)
        print(f"PROCESSOR {processor}")
        print("=" * 65)

        print(
            f"Noisy MAE          : "
            f"{noisy_mae:.6f}"
        )

        print(
            f"Mitigated MAE      : "
            f"{mitigated_mae:.6f}"
        )

        print(
            f"MAE improvement    : "
            f"{mae_improvement:.6f}"
        )

        print()

        print(
            f"Noisy RMSE         : "
            f"{noisy_rmse:.6f}"
        )

        print(
            f"Mitigated RMSE     : "
            f"{mitigated_rmse:.6f}"
        )

        print(
            f"RMSE improvement   : "
            f"{rmse_improvement:.6f}"
        )

        summary.append({
            "processor": processor,
            "noisy_mae": float(noisy_mae),
            "mitigated_mae": float(
                mitigated_mae
            ),
            "mae_improvement": float(
                mae_improvement
            ),
            "noisy_rmse": float(
                noisy_rmse
            ),
            "mitigated_rmse": float(
                mitigated_rmse
            ),
            "rmse_improvement": float(
                rmse_improvement
            ),
        })

    summary_df = pd.DataFrame(
        summary
    )

    output_path = (
        ROOT
        / "results"
        / "tables"
        / "mitigation_quality.csv"
    )

    summary_df.to_csv(
        output_path,
        index=False,
    )

    print()
    print("=" * 65)
    print("FINAL PROBABILITY-LEVEL COMPARISON")
    print("=" * 65)
    print()

    print(
        summary_df.to_string(
            index=False
        )
    )

    print()

    for row in summary:

        processor = row["processor"]

        if row["mae_improvement"] > 0:

            print(
                f"[OK] Processor {processor}: "
                f"mitigation reduced probability MAE."
            )

        elif row["mae_improvement"] == 0:

            print(
                f"[INFO] Processor {processor}: "
                f"probability MAE was unchanged."
            )

        else:

            print(
                f"[INFO] Processor {processor}: "
                f"mitigation increased probability MAE."
            )

    print()
    print(
        f"[OK] Analysis saved: "
        f"{output_path}"
    )

    print()
    print(
        "Mitigation quality analysis completed."
    )


if __name__ == "__main__":
    main()