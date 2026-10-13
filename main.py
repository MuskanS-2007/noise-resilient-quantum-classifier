"""QuantumShield - QFF 2026 Phase 1 entry point."""

from src.validate_setup import main as validate_setup


def main():
    print("=" * 65)
    print("QuantumShield | QFF 2026 | PS-Q3")
    print("Noise-Resilient Classification & Error Mitigation")
    print("=" * 65)

    print("\nValidating project configuration...")
    validate_setup()

    print("\nCore experiment modules:")
    print("  python -m src.train_vqc")
    print("  python -m src.benchmark_routing")
    print("  python -m src.benchmark_noise")
    print("  python -m src.benchmark_mitigation")
    print("  python -m src.analyze_mitigation")
    print("  python -m src.repeated_benchmark")
    print("  python -m src.architecture_stress")
    print("  python -m src.create_final_figures")

    print("\nFor the judge-facing walkthrough, open main.ipynb.")
    print("\nQuantumShield setup validation completed.")


if __name__ == "__main__":
    main()