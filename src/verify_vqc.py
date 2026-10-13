"""
Verify the QuantumShield 4-qubit VQC.
"""

from pathlib import Path

from src.vqc import build_vqc


ROOT = Path(__file__).resolve().parents[1]


def main():

    print()
    print("QuantumShield — VQC Circuit Verification")
    print("=" * 55)

    circuit, x, theta = build_vqc()

    print()
    print("Circuit information")
    print("-------------------")

    print(f"Number of qubits          : {circuit.num_qubits}")
    print(f"Input parameters          : {len(x)}")
    print(f"Trainable parameters      : {len(theta)}")
    print(f"Total circuit parameters  : {circuit.num_parameters}")

    print()
    print("Logical circuit depth")
    print("---------------------")

    print(f"Depth                     : {circuit.depth()}")

    print()
    print("Gate counts")
    print("-----------")

    gate_counts = circuit.count_ops()

    for gate, count in gate_counts.items():
        print(f"{gate:<25} : {count}")

    print()
    print("Logical VQC circuit")
    print("-------------------")
    print()

    print(circuit.draw(output="text"))

    output_dir = ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "logical_vqc.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(str(circuit.draw(output="text")))

    print()
    print(f"[OK] Circuit saved to: {output_file}")

    print()
    print("VQC verification completed.")


if __name__ == "__main__":
    main()