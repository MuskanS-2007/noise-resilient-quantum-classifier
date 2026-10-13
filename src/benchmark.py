"""QuantumShield benchmark summary utilities."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def load_final_results():
    """Load the primary saved benchmark summaries."""

    return {
        "routing": pd.read_csv(
            TABLES / "routing_benchmark.csv"
        ),
        "noise": pd.read_csv(
            TABLES / "noisy_benchmark.csv"
        ),
        "mitigation": pd.read_csv(
            TABLES / "mitigation_quality.csv"
        ),
        "repeated_seeds": pd.read_csv(
            TABLES / "repeated_seed_summary.csv"
        ),
        "architecture": pd.read_csv(
            TABLES / "architecture_stress.csv"
        ),
    }


def main():
    print("\nQuantumShield - Final Benchmark Summary")
    print("=" * 65)

    results = load_final_results()

    for name, dataframe in results.items():
        print()
        print(name.upper())
        print("-" * 65)
        print(dataframe.to_string(index=False))


if __name__ == "__main__":
    main()