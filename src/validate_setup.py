"""Validate the QuantumShield Phase 1 project configuration."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRECTORIES = [
    "data/raw",
    "data/processed",
    "results/tables",
    "results/figures",
    "processors",
    "src",
]

REQUIRED_PROCESSORS = [
    "processor_A.json",
    "processor_B.json",
]


def validate_directories():
    for relative_path in REQUIRED_DIRECTORIES:
        path = ROOT / relative_path

        if not path.exists():
            raise FileNotFoundError(
                f"Required directory missing: {relative_path}"
            )

        print(f"[OK] directory: {relative_path}")


def validate_processors():
    for name in REQUIRED_PROCESSORS:
        path = ROOT / "processors" / name

        if not path.exists():
            raise FileNotFoundError(
                f"Processor configuration missing: {name}"
            )

        with open(path, "r", encoding="utf-8") as file:
            config = json.load(file)

        required_keys = {
            "num_qubits",
            "coupling_map",
            "basis_gates",
        }

        missing = required_keys - set(config)

        if missing:
            raise ValueError(
                f"{name} missing required fields: "
                f"{sorted(missing)}"
            )

        print(
            f"[OK] {name}: "
            f"{config['num_qubits']} qubits, "
            f"{len(config['coupling_map'])} directed couplings"
        )


def main():
    validate_directories()
    validate_processors()

    print()
    print(
        "[OK] QuantumShield Phase 1 "
        "configuration validated."
    )


if __name__ == "__main__":
    main()