"""Processor definition loading and validation."""
import json
from pathlib import Path

def load_processor(path):
    """
    Load and validate QuantumShield processor configuration files.
    """
    path = Path(path)
    config = json.loads(path.read_text(encoding="utf-8"))
    required = ("name", "num_qubits", "coupling_map", "basis_gates")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError(f"{path} is missing required fields: {missing}")
    return config
