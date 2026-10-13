"""
QuantumShield — QFF 2026
PS-Q3: Noise-Resilient Classification & Error Mitigation

4-qubit Variational Quantum Classifier circuit.
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector


NUM_QUBITS = 4


def build_vqc():
    """
    Construct a parameterized 4-qubit VQC.

    Circuit structure:
    1. Angle encoding using RY(x_i)
    2. Trainable RY(theta_i) rotations
    3. CX entangling layer
    4. Second trainable RY layer

    Returns:
        circuit
        input_parameters
        weight_parameters
    """

    circuit = QuantumCircuit(NUM_QUBITS)

    # -------------------------------------------------
    # Input/data parameters
    # -------------------------------------------------

    x = ParameterVector("x", NUM_QUBITS)

    # -------------------------------------------------
    # Trainable VQC parameters
    # -------------------------------------------------

    theta = ParameterVector("theta", 2 * NUM_QUBITS)

    # -------------------------------------------------
    # 1. Angle encoding
    # -------------------------------------------------

    for qubit in range(NUM_QUBITS):
        circuit.ry(x[qubit], qubit)

    circuit.barrier()

    # -------------------------------------------------
    # 2. First trainable rotation layer
    # -------------------------------------------------

    for qubit in range(NUM_QUBITS):
        circuit.ry(theta[qubit], qubit)

    circuit.barrier()

    # -------------------------------------------------
    # 3. Entanglement layer
    # -------------------------------------------------

    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)

    circuit.barrier()

    # -------------------------------------------------
    # 4. Second trainable rotation layer
    # -------------------------------------------------

    for qubit in range(NUM_QUBITS):
        circuit.ry(theta[NUM_QUBITS + qubit], qubit)

    return circuit, x, theta


def build_measured_vqc():
    """
    Return the VQC with measurements on all four qubits.
    """

    circuit, x, theta = build_vqc()

    measured_circuit = circuit.copy()
    measured_circuit.measure_all()

    return measured_circuit, x, theta