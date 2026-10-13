"""
QuantumShield — QFF 2026
Processor A/B routing benchmark.
"""

import json
from pathlib import Path

import pandas as pd

from src.vqc import build_vqc
from src.routing import (
    load_processor,
    transpile_for_processor,
    circuit_metrics,
)


ROOT = Path(__file__).resolve().parents[1]


def main():

    print()
    print("QuantumShield — Processor A/B Routing Benchmark")
    print("=" * 60)

    logical_circuit, _, _ = build_vqc()

    logical_metrics = circuit_metrics(
        logical_circuit
    )

    print()
    print("Logical circuit")
    print("---------------")

    print(
        f"Depth       : {logical_metrics['depth']}"
    )

    print(
        f"CX count    : {logical_metrics['cx_count']}"
    )

    results = []

    for processor_name in ["A", "B"]:

        print()
        print("=" * 60)
        print(f"PROCESSOR {processor_name}")
        print("=" * 60)

        config = load_processor(
            processor_name
        )

        compiled = transpile_for_processor(
            logical_circuit,
            processor_name,
        )

        metrics = circuit_metrics(
            compiled
        )

        print(
            f"Physical qubits : "
            f"{config['num_qubits']}"
        )

        print(
            f"Depth           : "
            f"{metrics['depth']}"
        )

        print(
            f"CX count        : "
            f"{metrics['cx_count']}"
        )

        print(
            f"SWAP count      : "
            f"{metrics['swap_count']}"
        )

        print(
            f"RZ count        : "
            f"{metrics['rz_count']}"
        )

        print(
            f"SX count        : "
            f"{metrics['sx_count']}"
        )

        print(
            f"X count         : "
            f"{metrics['x_count']}"
        )

        print(
            f"Total gates     : "
            f"{metrics['total_gates']}"
        )

        cx_overhead = (
            metrics["cx_count"]
            - logical_metrics["cx_count"]
        )

        depth_overhead = (
            metrics["depth"]
            - logical_metrics["depth"]
        )

        print()
        print(
            f"CX overhead     : "
            f"{cx_overhead:+d}"
        )

        print(
            f"Depth overhead  : "
            f"{depth_overhead:+d}"
        )

        results.append({
            "processor": processor_name,
            "physical_qubits": config[
                "num_qubits"
            ],
            "logical_depth": logical_metrics[
                "depth"
            ],
            "transpiled_depth": metrics[
                "depth"
            ],
            "logical_cx": logical_metrics[
                "cx_count"
            ],
            "transpiled_cx": metrics[
                "cx_count"
            ],
            "cx_overhead": cx_overhead,
            "swap_count_final_basis": metrics[
                "swap_count"
            ],
            "rz_count": metrics[
                "rz_count"
            ],
            "sx_count": metrics[
                "sx_count"
            ],
            "x_count": metrics[
                "x_count"
            ],
            "total_gates": metrics[
                "total_gates"
            ],
        })

        output_dir = (
            ROOT
            / "results"
            / "tables"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        circuit_path = (
            output_dir
            / f"processor_{processor_name}_transpiled.txt"
        )

        with open(
            circuit_path,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(
                str(
                    compiled.draw(
                        output="text"
                    )
                )
            )

        print()
        print(
            f"[OK] Circuit saved: "
            f"{circuit_path}"
        )

    results_dir = (
        ROOT
        / "results"
        / "tables"
    )

    dataframe = pd.DataFrame(
        results
    )

    csv_path = (
        results_dir
        / "routing_benchmark.csv"
    )

    dataframe.to_csv(
        csv_path,
        index=False,
    )

    json_path = (
        results_dir
        / "routing_benchmark.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
        )

    print()
    print("=" * 60)
    print("A/B COMPARISON")
    print("=" * 60)
    print()

    print(
        dataframe[
            [
                "processor",
                "physical_qubits",
                "transpiled_depth",
                "transpiled_cx",
                "cx_overhead",
            ]
        ].to_string(index=False)
    )

    print()
    print(
        f"[OK] Benchmark CSV saved: "
        f"{csv_path}"
    )

    print()
    print(
        "Processor A/B routing benchmark completed."
    )


if __name__ == "__main__":
    main()