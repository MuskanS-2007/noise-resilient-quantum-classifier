"""
QuantumShield — QFF 2026
Official Phase-1 synthetic noise model.
"""

from qiskit_aer.noise import (
    NoiseModel,
    ReadoutError,
    depolarizing_error,
)


SINGLE_QUBIT_ERROR = 0.001
CX_ERROR = 0.005
READOUT_ERROR = 0.01


def build_noise_model():
    """
    Build the QFF Phase-1 synthetic noise model.

    Official parameters:
    - 1-qubit depolarizing error: 0.001
    - CX depolarizing error:     0.005
    - Readout error:             0.01
    """

    noise_model = NoiseModel()

    # ---------------------------------------------
    # Single-qubit depolarizing noise
    # ---------------------------------------------

    single_qubit_error = depolarizing_error(
        SINGLE_QUBIT_ERROR,
        1,
    )

    for gate in ["rz", "sx", "x"]:
        noise_model.add_all_qubit_quantum_error(
            single_qubit_error,
            gate,
        )

    # ---------------------------------------------
    # Two-qubit CX depolarizing noise
    # ---------------------------------------------

    cx_error = depolarizing_error(
        CX_ERROR,
        2,
    )

    noise_model.add_all_qubit_quantum_error(
        cx_error,
        "cx",
    )

    # ---------------------------------------------
    # Symmetric readout error
    # ---------------------------------------------

    readout_error = ReadoutError(
        [
            [1 - READOUT_ERROR, READOUT_ERROR],
            [READOUT_ERROR, 1 - READOUT_ERROR],
        ]
    )

    noise_model.add_all_qubit_readout_error(
        readout_error
    )

    return noise_model