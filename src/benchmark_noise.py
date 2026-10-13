"""
QuantumShield — QFF 2026
Noisy Processor A/B classification benchmark.
"""

from pathlib import Path
import json

from matplotlib.pylab import sample
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from qiskit_aer import AerSimulator

from src.problem import prepare_q3_dataset
from src.classifier import bind_vqc
from src.routing import transpile_for_processor
from src.noise import build_noise_model


ROOT = Path(__file__).resolve().parents[1]

SHOTS = 4096
SIMULATOR_SEED = 42


def noisy_predict(
    sample,
    weights,
    processor_name,
    simulator,
    simulator_seed=42,
    ):    
    """
    Run one frozen VQC sample under the official synthetic noise.
    Classification uses measurement of logical qubit 0.
    """

    circuit = bind_vqc(sample, weights)

    # Measure logical qubit 0 only.
    circuit.measure_all()

    compiled = transpile_for_processor(
        circuit,
        processor_name,
    )

    job = simulator.run(
        compiled,
        shots=SHOTS,
        seed_simulator=simulator_seed,
    )

    counts = job.result().get_counts()

    total = sum(counts.values())

    # measure_all() creates four classical bits.
    # Qiskit displays bitstrings as q3 q2 q1 q0,
    # therefore the rightmost bit corresponds to q0.
    class_1_counts = sum(
        count
        for bitstring, count in counts.items()
        if bitstring.replace(" ", "")[-1] == "1"
    )

    probability_1 = class_1_counts / total

    prediction = int(
        probability_1 >= 0.5
    )

    return prediction, probability_1


def main():

    print()
    print("QuantumShield — Noisy A/B Classification Benchmark")
    print("=" * 65)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    weights_path = (
        ROOT
        / "results"
        / "tables"
        / "trained_vqc_weights.npy"
    )

    if not weights_path.exists():
        raise FileNotFoundError(
            "Trained VQC weights were not found. "
            "Run python -m src.train_vqc first."
        )

    weights = np.load(weights_path)

    print()
    print(f"Test samples       : {len(X_test)}")
    print(f"Shots/sample       : {SHOTS}")
    print(f"Simulator seed     : {SIMULATOR_SEED}")
    print(f"Frozen weights     : loaded")
    print()

    noise_model = build_noise_model()

    simulator = AerSimulator(
        noise_model=noise_model
    )

    all_results = []
    summary = []

    for processor_name in ["A", "B"]:

        print("=" * 65)
        print(f"PROCESSOR {processor_name}")
        print("=" * 65)

        predictions = []
        probabilities = []

        for index, (sample, true_label) in enumerate(
            zip(X_test, y_test),
            start=1,
        ):

            prediction, probability = noisy_predict(
                sample,
                weights,
                processor_name,
                simulator,
            )

            predictions.append(prediction)
            probabilities.append(probability)

            print(
                f"Sample {index:02d}/{len(X_test)} | "
                f"True: {int(true_label)} | "
                f"P(1): {probability:.4f} | "
                f"Pred: {prediction}"
            )

            all_results.append({
                "processor": processor_name,
                "sample": index,
                "true_label": int(true_label),
                "probability_class_1": float(probability),
                "prediction": int(prediction),
                "shots": SHOTS,
            })

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        correct = int(
            np.sum(
                np.asarray(predictions)
                == np.asarray(y_test)
            )
        )

        print()
        print(
            f"Noisy accuracy : "
            f"{accuracy:.4f} "
            f"({accuracy * 100:.2f}%)"
        )

        print(
            f"Correct        : "
            f"{correct}/{len(y_test)}"
        )

        summary.append({
            "processor": processor_name,
            "shots": SHOTS,
            "accuracy": float(accuracy),
            "correct": correct,
            "total": int(len(y_test)),
        })

        print()

    # ---------------------------------------------
    # Save detailed results
    # ---------------------------------------------

    output_dir = (
        ROOT
        / "results"
        / "tables"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    detailed_path = (
        output_dir
        / "noisy_predictions.csv"
    )

    pd.DataFrame(
        all_results
    ).to_csv(
        detailed_path,
        index=False,
    )

    summary_path = (
        output_dir
        / "noisy_benchmark.csv"
    )

    summary_df = pd.DataFrame(
        summary
    )

    summary_df.to_csv(
        summary_path,
        index=False,
    )

    json_path = (
        output_dir
        / "noisy_benchmark.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
        )

    print("=" * 65)
    print("FINAL NOISY A/B COMPARISON")
    print("=" * 65)
    print()

    print(
        summary_df.to_string(
            index=False
        )
    )

    print()
    print(
        f"[OK] Detailed predictions saved: "
        f"{detailed_path}"
    )

    print(
        f"[OK] Benchmark summary saved: "
        f"{summary_path}"
    )

    print()
    print(
        "Noisy A/B classification benchmark completed."
    )


if __name__ == "__main__":
    main()