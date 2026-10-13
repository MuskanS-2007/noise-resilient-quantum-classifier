"""
QuantumShield — QFF 2026
Ideal VQC classifier utilities.
"""

import numpy as np

from qiskit.quantum_info import Statevector, SparsePauliOp

from src.vqc import build_vqc


def bind_vqc(sample, weights):
    """
    Bind one 4-feature sample and eight trainable weights
    to the parameterized VQC.
    """

    circuit, x_params, theta_params = build_vqc()

    if len(sample) != 4:
        raise ValueError("A sample must contain exactly 4 features.")

    if len(weights) != 8:
        raise ValueError("The VQC requires exactly 8 trainable weights.")

    parameter_values = {}

    for i in range(4):
        parameter_values[x_params[i]] = float(sample[i])

    for i in range(8):
        parameter_values[theta_params[i]] = float(weights[i])

    bound_circuit = circuit.assign_parameters(
        parameter_values,
        inplace=False,
    )

    return bound_circuit


def expectation_z0(sample, weights):
    """
    Calculate the ideal <Z> expectation value of qubit 0.
    """

    circuit = bind_vqc(sample, weights)

    state = Statevector.from_instruction(circuit)

    # Qiskit Pauli strings are ordered q3 q2 q1 q0.
    observable = SparsePauliOp.from_list([
        ("IIIZ", 1.0)
    ])

    expectation = state.expectation_value(observable)

    return float(np.real(expectation))


def probability_class_1(sample, weights):
    """
    Convert <Z0> into probability-like class-1 output.

    For a Z measurement:
        P(1) = (1 - <Z>) / 2
    """

    expectation = expectation_z0(sample, weights)

    probability = (1.0 - expectation) / 2.0

    return float(probability)


def predict(sample, weights):
    """
    Binary classification using threshold 0.5.
    """

    probability = probability_class_1(sample, weights)

    return int(probability >= 0.5)