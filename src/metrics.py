"""Common circuit resource metrics for QuantumShield."""


TWO_QUBIT_GATES = {
    "cx",
    "cz",
    "ecr",
    "swap",
    "rxx",
    "ryy",
    "rzz",
}


def circuit_metrics(compiled_circuit):
    """Return common resource metrics for a compiled circuit."""

    operations = compiled_circuit.count_ops()

    return {
        "depth": compiled_circuit.depth(),
        "physical_qubits": compiled_circuit.num_qubits,
        "total_operations": int(
            sum(operations.values())
        ),
        "two_qubit_gate_count_estimate": int(
            sum(
                count
                for gate, count in operations.items()
                if str(gate).lower() in TWO_QUBIT_GATES
            )
        ),
        "swap_count": int(
            operations.get("swap", 0)
        ),
        "operation_counts": {
            str(gate): int(count)
            for gate, count in operations.items()
        },
    }