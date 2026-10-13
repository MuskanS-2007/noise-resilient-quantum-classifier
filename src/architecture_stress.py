"""
QuantumShield — QFF 2026
Architecture connectivity stress test.

This experiment is separate from the trained Q3 classifier.
It evaluates routing overhead for a cyclic interaction pattern.
"""

from pathlib import Path
import pandas as pd

from qiskit import QuantumCircuit

from src.routing import (
    transpile_for_processor,
    circuit_metrics,
)


ROOT = Path(__file__).resolve().parents[1]


def build_ring_circuit():
    """
    Four-qubit cyclic interaction circuit.
    """

    circuit = QuantumCircuit(4)

    # Small single-qubit preparation layer.
    for qubit in range(4):
        circuit.ry(0.5, qubit)

    circuit.barrier()

    # Logical interaction ring.
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)
    circuit.cx(3, 0)

    circuit.barrier()

    return circuit


def main():

    print()
    print("QuantumShield — Architecture Stress Test")
    print("=" * 65)

    circuit = build_ring_circuit()

    logical = circuit_metrics(circuit)

    print()
    print("Logical ring circuit")
    print("--------------------")

    print(f"Depth    : {logical['depth']}")
    print(f"CX count : {logical['cx_count']}")

    results = []

    for processor in ["A", "B"]:

        compiled = transpile_for_processor(
            circuit,
            processor,
        )

        metrics = circuit_metrics(
            compiled
        )

        cx_overhead = (
            metrics["cx_count"]
            - logical["cx_count"]
        )

        print()
        print("=" * 65)
        print(f"PROCESSOR {processor}")
        print("=" * 65)

        print(
            f"Transpiled depth : "
            f"{metrics['depth']}"
        )

        print(
            f"CX count         : "
            f"{metrics['cx_count']}"
        )

        print(
            f"CX overhead      : "
            f"{cx_overhead:+d}"
        )

        print(
            f"Final-basis SWAP : "
            f"{metrics['swap_count']}"
        )

        results.append({
            "processor": processor,
            "logical_depth": logical["depth"],
            "transpiled_depth": metrics["depth"],
            "logical_cx": logical["cx_count"],
            "transpiled_cx": metrics["cx_count"],
            "cx_overhead": cx_overhead,
            "final_basis_swap": metrics["swap_count"],
        })

    dataframe = pd.DataFrame(results)

    output_path = (
        ROOT
        / "results"
        / "tables"
        / "architecture_stress.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    print()
    print("=" * 65)
    print("FINAL ARCHITECTURE COMPARISON")
    print("=" * 65)
    print()

    print(
        dataframe.to_string(
            index=False
        )
    )

    print()
    print(
        f"[OK] Results saved: {output_path}"
    )

    print()
    print(
        "Architecture stress test completed."
    )


if __name__ == "__main__":
    main()