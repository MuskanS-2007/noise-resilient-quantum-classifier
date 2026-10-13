"""
QuantumShield — QFF 2026
Readout error mitigation utilities.
"""

import numpy as np

from src.noise import READOUT_ERROR


def mitigate_readout_probability(
    observed_probability,
    readout_error=READOUT_ERROR,
):
    """
    Correct a measured P(1) assuming symmetric
    binary readout error.

    p_observed = e + (1 - 2e) * p_true
    """

    denominator = 1.0 - 2.0 * readout_error

    if denominator <= 0:
        raise ValueError(
            "Readout error must be below 0.5."
        )

    corrected = (
        observed_probability - readout_error
    ) / denominator

    return float(
        np.clip(corrected, 0.0, 1.0)
    )


def mitigated_prediction(observed_probability):
    """
    Correct P(1), then apply binary threshold.
    """

    corrected_probability = (
        mitigate_readout_probability(
            observed_probability
        )
    )

    prediction = int(
        corrected_probability >= 0.5
    )

    return prediction, corrected_probability