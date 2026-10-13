"""
QuantumShield — QFF 2026
Generate final submission figures from saved experiment results.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]

TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"

FIGURES.mkdir(
    parents=True,
    exist_ok=True,
)


def save_figure(filename):
    path = FIGURES / filename

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"[OK] Saved: {path}")


def plot_training_history():

    history = pd.read_json(
        TABLES / "training_history.json"
    )

    plt.figure(figsize=(8, 5))

    plt.plot(
        history["evaluation"],
        history["loss"],
    )

    plt.xlabel("Optimizer Evaluation")
    plt.ylabel("Binary Cross-Entropy Loss")
    plt.title("VQC Training Convergence")
    plt.grid(alpha=0.3)

    save_figure(
        "training_convergence.png"
    )


def plot_architecture_comparison():

    data = pd.read_csv(
        TABLES / "architecture_stress.csv"
    )

    x = np.arange(len(data))
    width = 0.35

    plt.figure(figsize=(8, 5))

    plt.bar(
        x - width / 2,
        data["transpiled_depth"],
        width,
        label="Transpiled Depth",
    )

    plt.bar(
        x + width / 2,
        data["transpiled_cx"],
        width,
        label="CX Count",
    )

    plt.xticks(
        x,
        [
            f"Processor {p}"
            for p in data["processor"]
        ],
    )

    plt.ylabel("Count")
    plt.title(
        "Architecture Stress Test: Routing Cost"
    )

    plt.legend()
    plt.grid(
        axis="y",
        alpha=0.3,
    )

    save_figure(
        "architecture_comparison.png"
    )


def plot_repeated_accuracy():

    data = pd.read_csv(
        TABLES / "repeated_seed_results.csv"
    )

    plt.figure(figsize=(8, 5))

    for processor in ["A", "B"]:

        subset = data[
            data["processor"] == processor
        ]

        plt.plot(
            subset["seed"].astype(str),
            subset["noisy_accuracy"] * 100,
            marker="o",
            label=f"Processor {processor}",
        )

    plt.xlabel("Simulator Seed")
    plt.ylabel("Test Accuracy (%)")

    plt.title(
        "Noisy VQC Accuracy Across Simulator Seeds"
    )

    plt.legend()
    plt.grid(alpha=0.3)

    save_figure(
        "repeated_seed_accuracy.png"
    )


def plot_mitigation_mae():

    data = pd.read_csv(
        TABLES / "repeated_seed_results.csv"
    )

    # A/B are identical for the baseline classifier,
    # so use Processor A to avoid overlapping curves.
    subset = data[
        data["processor"] == "A"
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        subset["seed"].astype(str),
        subset["noisy_mae"],
        marker="o",
        label="Noisy",
    )

    plt.plot(
        subset["seed"].astype(str),
        subset["mitigated_mae"],
        marker="o",
        label="Readout Mitigated",
    )

    plt.xlabel("Simulator Seed")
    plt.ylabel(
        "MAE vs Ideal Probability"
    )

    plt.title(
        "Readout Mitigation Reduces Probability Error"
    )

    plt.legend()
    plt.grid(alpha=0.3)

    save_figure(
        "mitigation_mae.png"
    )


def main():

    print()
    print(
        "QuantumShield — Final Figure Generation"
    )

    print("=" * 60)
    print()

    plot_training_history()
    plot_architecture_comparison()
    plot_repeated_accuracy()
    plot_mitigation_mae()

    print()
    print(
        "Final figure generation completed."
    )


if __name__ == "__main__":
    main()