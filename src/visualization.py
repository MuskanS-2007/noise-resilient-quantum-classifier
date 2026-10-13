"""Visualization utilities for saved QuantumShield results."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def plot_architecture_results(
    csv_path=None,
    output_path=None,
):
    """Plot transpiled depth and CX count for the stress test."""

    if csv_path is None:
        csv_path = (
            ROOT
            / "results"
            / "tables"
            / "architecture_stress.csv"
        )

    if output_path is None:
        output_path = (
            ROOT
            / "results"
            / "figures"
            / "architecture_comparison.png"
        )

    dataframe = pd.read_csv(csv_path)

    required = {
        "processor",
        "transpiled_depth",
        "transpiled_cx",
    }

    if not required.issubset(dataframe.columns):
        raise ValueError(
            "Architecture result table is missing required columns."
        )

    plot_data = dataframe.set_index("processor")[
        ["transpiled_depth", "transpiled_cx"]
    ]

    axis = plot_data.plot(
        kind="bar",
        figsize=(8, 5),
    )

    axis.set_title(
        "Architecture Stress Test: Routing Cost"
    )
    axis.set_xlabel("Processor")
    axis.set_ylabel("Count")

    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    return output_path