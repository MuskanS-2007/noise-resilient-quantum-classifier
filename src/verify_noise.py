"""
Verify the QuantumShield synthetic noise model.
"""

from src.noise import (
    build_noise_model,
    SINGLE_QUBIT_ERROR,
    CX_ERROR,
    READOUT_ERROR,
)


def main():

    print()
    print("QuantumShield — Synthetic Noise Verification")
    print("=" * 60)

    noise_model = build_noise_model()

    print()
    print("Official Phase-1 noise parameters")
    print("---------------------------------")

    print(
        f"1-qubit depolarizing error : "
        f"{SINGLE_QUBIT_ERROR}"
    )

    print(
        f"CX depolarizing error      : "
        f"{CX_ERROR}"
    )

    print(
        f"Readout error              : "
        f"{READOUT_ERROR}"
    )

    print()
    print("Affected instructions")
    print("---------------------")

    print(
        sorted(
            noise_model.noise_instructions
        )
    )

    print()
    print("Noise model summary")
    print("-------------------")

    print(noise_model)

    print()

    required = {
        "rz",
        "sx",
        "x",
        "cx",
        "measure",
    }

    actual = set(
        noise_model.noise_instructions
    )

    if required.issubset(actual):

        print(
            "[OK] All required noisy operations "
            "are configured."
        )

    else:

        print(
            "[ERROR] Some required noisy "
            "operations are missing."
        )

        print(
            "Missing:",
            required - actual,
        )

    print()
    print(
        "Synthetic noise verification completed."
    )


if __name__ == "__main__":
    main()