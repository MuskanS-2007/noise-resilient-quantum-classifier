"""
QuantumShield — QFF 2026
Processor-aware transpilation and routing.
"""

import json
from pathlib import Path

from qiskit import transpile
from qiskit.transpiler import CouplingMap


ROOT = Path(__file__).resolve().parents[1]


def load_processor(name):
    """
    Load Processor A or Processor B configuration.
    """

    path = ROOT / "processors" / f"processor_{name}.json"

    with open(path, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config


def transpile_for_processor(circuit, processor_name):
    """
    Transpile a logical circuit using the selected processor's
    coupling map and the official Phase-1 baseline settings.
    """

    config = load_processor(processor_name)

    coupling_map = CouplingMap(
        couplinglist=config["coupling_map"]
    )

    compiled = transpile(
        circuit,
        basis_gates=config["basis_gates"],
        coupling_map=coupling_map,
        optimization_level=1,
        seed_transpiler=42,
    )

    return compiled


def circuit_metrics(circuit):
    """
    Extract architecture/resource metrics.
    """

    operations = circuit.count_ops()

    return {
        "depth": int(circuit.depth()),
        "cx_count": int(operations.get("cx", 0)),
        "swap_count": int(operations.get("swap", 0)),
        "rz_count": int(operations.get("rz", 0)),
        "sx_count": int(operations.get("sx", 0)),
        "x_count": int(operations.get("x", 0)),
        "total_gates": int(
            sum(operations.values())
        ),
    }