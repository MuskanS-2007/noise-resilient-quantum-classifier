"""
Verify the official QuantumShield Q3 synthetic dataset.
"""

from src.problem import prepare_q3_dataset, save_dataset


def main():

    print()
    print("QuantumShield — Q3 Dataset Verification")
    print("=" * 50)

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
    ) = prepare_q3_dataset()

    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")

    print(f"Features/sample  : {X_train.shape[1]}")

    print()
    print("Class distribution")

    print(
        f"Training -> class 0: {(y_train == 0).sum()}, "
        f"class 1: {(y_train == 1).sum()}"
    )

    print(
        f"Testing  -> class 0: {(y_test == 0).sum()}, "
        f"class 1: {(y_test == 1).sum()}"
    )

    print()
    print("Angle-encoded feature range")

    print(
        f"Training minimum : {X_train.min():.6f}"
    )

    print(
        f"Training maximum : {X_train.max():.6f}"
    )

    raw_path, train_path, test_path = save_dataset()

    print()
    print("[OK] Dataset files generated")

    print(f"Raw data       : {raw_path}")
    print(f"Training data  : {train_path}")
    print(f"Testing data   : {test_path}")

    print()
    print("Dataset verification completed.")


if __name__ == "__main__":
    main()