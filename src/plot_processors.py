import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


ROOT = Path(__file__).resolve().parents[1]


def load_processor(filename):
    path = ROOT / "processors" / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def unique_edges(coupling_map):
    """Convert directed coupling edges into unique physical connections."""
    edges = set()

    for q1, q2 in coupling_map:
        edges.add(tuple(sorted((q1, q2))))

    return sorted(edges)


def draw_processor(config, output_filename):
    graph = nx.Graph()

    graph.add_nodes_from(range(config["num_qubits"]))
    graph.add_edges_from(unique_edges(config["coupling_map"]))

    plt.figure(figsize=(7, 5))

    positions = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        positions,
        with_labels=True,
        labels={q: f"q{q}" for q in graph.nodes()},
        node_size=1800,
        font_size=12,
        font_weight="bold"
    )

    plt.title(
        f'{config["name"]}\n'
        f'{config["num_qubits"]} physical qubits | '
        f'{graph.number_of_edges()} physical connections'
    )

    output_path = ROOT / "results" / "figures" / output_filename

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f'[OK] {config["name"]}')
    print(f'     Physical qubits: {config["num_qubits"]}')
    print(f'     Unique connections: {graph.number_of_edges()}')
    print(f'     Connections: {unique_edges(config["coupling_map"])}')
    print(f'     Figure saved: {output_path}')


def main():
    processor_a = load_processor("processor_A.json")
    processor_b = load_processor("processor_B.json")

    print("\nQuantumShield — Processor Topology Verification")
    print("=" * 50)

    draw_processor(
        processor_a,
        "processor_A_topology.png"
    )

    print()

    draw_processor(
        processor_b,
        "processor_B_topology.png"
    )

    print("\nTopology verification completed.")


if __name__ == "__main__":
    main()