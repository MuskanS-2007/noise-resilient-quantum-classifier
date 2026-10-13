"""
QuantumShield — QFF 2026
Readout-error mitigation benchmark.
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score

from src.mitigation import mitigated_prediction


ROOT = Path(__file__).resolve().parents[1]


def main():

    print()
    print("QuantumShield — Readout Mitigation Benchmark")
    print("=" * 65)

    input_path = (
        ROOT
        / "results"
        / "tables"
        / "noisy_predictions.csv"
    )

    if not input_path.exists():
        raise FileNotFoundError(
            "noisy_predictions.csv not found. "
            "Run the noisy benchmark first."
        )

    dataframe = pd.read_csv(input_path)

    mitigated_probabilities = []
    mitigated_predictions = []

    for probability in dataframe[
        "probability_class_1"
    ]:

        prediction, corrected = (
            mitigated_prediction(
                probability
            )
        )

        mitigated_probabilities.append(
            corrected
        )

        mitigated_predictions.append(
            prediction
        )

    dataframe[
        "mitigated_probability_class_1"
    ] = mitigated_probabilities

    dataframe[
        "mitigated_prediction"
    ] = mitigated_predictions

    summary = []

    for processor in ["A", "B"]:

        subset = dataframe[
            dataframe["processor"] == processor
        ].copy()

        noisy_accuracy = accuracy_score(
            subset["true_label"],
            subset["prediction"],
        )

        mitigated_accuracy = accuracy_score(
            subset["true_label"],
            subset["mitigated_prediction"],
        )

        changed = int(
            (
                subset["prediction"]
                != subset["mitigated_prediction"]
            ).sum()
        )

        print()
        print("=" * 65)
        print(f"PROCESSOR {processor}")
        print("=" * 65)

        print(
            f"Noisy accuracy      : "
            f"{noisy_accuracy:.4f} "
            f"({noisy_accuracy * 100:.2f}%)"
        )

        print(
            f"Mitigated accuracy  : "
            f"{mitigated_accuracy:.4f} "
            f"({mitigated_accuracy * 100:.2f}%)"
        )

        print(
            f"Changed predictions : {changed}"
        )

        summary.append({
            "processor": processor,
            "noisy_accuracy": float(
                noisy_accuracy
            ),
            "mitigated_accuracy": float(
                mitigated_accuracy
            ),
            "accuracy_change": float(
                mitigated_accuracy
                - noisy_accuracy
            ),
            "changed_predictions": changed,
        })

    output_dir = (
        ROOT
        / "results"
        / "tables"
    )

    detailed_path = (
        output_dir
        / "mitigated_predictions.csv"
    )

    dataframe.to_csv(
        detailed_path,
        index=False,
    )

    summary_df = pd.DataFrame(summary)

    summary_path = (
        output_dir
        / "mitigation_benchmark.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
    )

    print()
    print("=" * 65)
    print("FINAL MITIGATION COMPARISON")
    print("=" * 65)
    print()

    print(
        summary_df.to_string(
            index=False
        )
    )

    print()
    print(
        f"[OK] Detailed results saved: "
        f"{detailed_path}"
    )

    print(
        f"[OK] Summary saved: "
        f"{summary_path}"
    )

    print()
    print(
        "Readout mitigation benchmark completed."
    )


if __name__ == "__main__":
    main()
    