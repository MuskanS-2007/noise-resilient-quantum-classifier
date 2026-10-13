"""
Verify one ideal QuantumShield VQC prediction.
"""

import numpy as np

from src.problem import prepare_q3_dataset
from src.classifier import (
    bind_vqc,
    expectation_z0,
    probability_class_1,
    predict,
)


def main():

    print()
    print("QuantumShield — Ideal Classifier Verification")
    print("=" * 55)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    # Deterministic initial weights.
    rng = np.random.default_rng(42)

    weights = rng.uniform(
        low=-np.pi,
        high=np.pi,
        size=8,
    )

    sample = X_train[0]
    true_label = y_train[0]

    circuit = bind_vqc(sample, weights)

    expectation = expectation_z0(sample, weights)
    probability = probability_class_1(sample, weights)
    prediction = predict(sample, weights)

    print()
    print("Dataset sample")
    print("--------------")

    print(f"Features       : {np.round(sample, 4)}")
    print(f"True label     : {true_label}")

    print()
    print("Initial VQC weights")
    print("-------------------")

    print(np.round(weights, 4))

    print()
    print("Bound circuit")
    print("-------------")

    print(f"Remaining parameters : {circuit.num_parameters}")
    print(f"Circuit depth        : {circuit.depth()}")

    print()
    print("Ideal quantum output")
    print("--------------------")

    print(f"<Z0>                 : {expectation:.6f}")
    print(f"P(class 1)           : {probability:.6f}")
    print(f"Predicted class      : {prediction}")
    print(f"True class           : {true_label}")

    print()

    if circuit.num_parameters == 0:
        print("[OK] All VQC parameters successfully bound.")
    else:
        print("[ERROR] Circuit still contains unbound parameters.")

    if -1.0 <= expectation <= 1.0:
        print("[OK] Expectation value is physically valid.")
    else:
        print("[ERROR] Invalid expectation value.")

    if 0.0 <= probability <= 1.0:
        print("[OK] Classification probability is valid.")
    else:
        print("[ERROR] Invalid classification probability.")

    print()
    print("Ideal classifier verification completed.")


if __name__ == "__main__":
    main()