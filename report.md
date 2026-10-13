# QuantumShield - Phase 1 Technical Report

## PS-Q3: Noise-Resilient Classification & Error Mitigation

## 1. Objective

QuantumShield investigates the reliability of a Variational Quantum Classifier (VQC) under synthetic quantum-device noise and different processor connectivity constraints.

The project has three primary objectives:

1. Build and train a reproducible 4-qubit VQC for binary classification.
2. Evaluate the classifier under identical synthetic noise on Processor A and Processor B and apply readout error mitigation.
3. Analyze how processor connectivity influences circuit routing, CX overhead, and transpiled depth.

The experiments deliberately separate noise effects from architectural effects by using identical noise parameters for both processors.

---

## 2. Dataset and Preprocessing

A deterministic synthetic binary-classification dataset containing 200 samples and four features was generated using `make_classification`.

Configuration:

* Samples: 200
* Features: 4
* Informative features: 3
* Classes: 2
* Random state: 42
* Training samples: 160
* Testing samples: 40

The training and testing sets are class-balanced.

Features are scaled to the interval `[0, pi]` for quantum angle encoding.

---

## 3. Variational Quantum Classifier

The logical VQC uses four qubits.

Each input feature is encoded using an `RY` rotation. The variational portion contains eight trainable rotation parameters and a CX entanglement structure.

The model is optimized using COBYLA with binary cross-entropy as the training objective.

The classifier is trained once using ideal statevector simulation. Its trained parameters are then frozen and reused for all processor and noise experiments.

This ensures that Processor A and Processor B are evaluated using the same learned quantum model.

### Ideal Result

The trained classifier achieved:

**Ideal test accuracy: 77.5%**

The optimizer used 80 objective evaluations.

---

## 4. Processor Configurations

Two processor architectures are evaluated.

### Processor A

* 5 physical qubits
* Sparse branching/tree-style connectivity

### Processor B

* 9 physical qubits
* Sparse heavy-hex-inspired connectivity

Both processors use the basis-gate set:

`rz, sx, x, cx`

Transpilation uses:

* Optimization level: 1
* Transpiler seed: 42

---

## 5. Baseline Routing Analysis

The trained classifier has a simple chain-like logical interaction pattern.

Both Processor A and Processor B contain a physical path capable of embedding this interaction pattern efficiently.

The resulting baseline transpilation produced:

| Metric              | Processor A | Processor B |
| ------------------- | ----------: | ----------: |
| Logical CX count    |           3 |           3 |
| Transpiled CX count |           3 |           3 |
| CX overhead         |           0 |           0 |
| Transpiled depth    |          15 |          15 |

This result demonstrates that a larger or more connected processor does not automatically provide an advantage for every quantum circuit.

---

## 6. Synthetic Noise Model

Both processors are evaluated using the same synthetic noise model.

| Noise source                    | Error rate |
| ------------------------------- | ---------: |
| Single-qubit depolarizing error |      0.001 |
| CX depolarizing error           |      0.005 |
| Readout error                   |       0.01 |

Noisy experiments use 4096 shots.

Using identical noise rates ensures that observed architectural differences are not caused by assigning different physical error strengths to the processors.

---

## 7. Noisy Classification

For simulator seed 42, both processors produced:

**Noisy test accuracy: 80.0%**

This value is slightly higher than the 77.5% ideal test accuracy.

However, this should not be interpreted as evidence that quantum noise improves classification.

The test set contains only 40 samples, and several predicted probabilities lie close to the 0.5 classification threshold. Finite-shot sampling can therefore change a small number of hard predictions.

A repeated-seed experiment was performed to quantify this variability.

---

## 8. Readout Error Mitigation

QuantumShield applies symmetric readout-error correction to the observed class-1 probabilities.

For readout error rate `e` and observed probability `p_obs`:

`p_corrected = (p_obs - e) / (1 - 2e)`

The corrected value is clipped to the interval `[0, 1]`.

Because this symmetric transformation preserves the 0.5 decision boundary, mitigation is not expected to necessarily change hard classification labels.

Therefore, mitigation is evaluated using probability-level error relative to exact ideal statevector predictions.

### Seed-42 Results

| Metric                    |    Noisy | Mitigated |
| ------------------------- | -------: | --------: |
| Accuracy                  |    80.0% |     80.0% |
| MAE vs ideal probability  | 0.007789 |  0.004656 |
| RMSE vs ideal probability | 0.009903 |  0.006018 |

For this run, mitigation reduced MAE by approximately 40.2% and RMSE by approximately 39.2%.

---

## 9. Repeated-Seed Robustness

To avoid drawing conclusions from a single stochastic realization, the noisy experiment was repeated using five simulator seeds:

`42, 123, 256, 512, 1024`

Each run used 4096 shots.

The noisy accuracies were:

* Seed 42: 80.0%
* Seed 123: 80.0%
* Seed 256: 82.5%
* Seed 512: 77.5%
* Seed 1024: 75.0%

Across the five runs:

* Mean noisy accuracy: **79.0%**
* Accuracy standard deviation: **2.85 percentage points**
* Mean noisy probability MAE: **0.009598**
* Mean mitigated probability MAE: **0.006276**

This corresponds to an approximately **34.6% relative reduction in mean probability MAE**.

Mitigation reduced probability MAE for every tested simulator seed.

Hard-label accuracy remained unchanged by the symmetric readout correction.

---

## 10. Processor Connectivity Stress Test

The baseline classifier did not expose an architectural difference because its chain-like interaction graph could be embedded efficiently on both processors.

To analyze connectivity separately, QuantumShield uses an additional four-qubit cyclic interaction circuit.

The stress circuit contains the logical interactions:

`0-1, 1-2, 2-3, 3-0`

This experiment is used only for architectural analysis and does not replace or retrain the classifier.

### Results

| Metric              | Processor A | Processor B |
| ------------------- | ----------: | ----------: |
| Logical depth       |           5 |           5 |
| Logical CX count    |           4 |           4 |
| Transpiled depth    |          11 |           8 |
| Transpiled CX count |           7 |           4 |
| CX overhead         |          +3 |           0 |

Processor B required approximately **42.9% fewer transpiled CX gates** than Processor A for this workload.

Its transpiled depth was approximately **27.3% lower**.

The final native-basis circuit contains no explicit SWAP instruction because routing operations are decomposed into native CX operations. The additional three CX gates on Processor A therefore provide the relevant routing-overhead evidence.

---

## 11. Discussion

The experiments produce three main observations.

### Error mitigation should not be judged only by accuracy

Readout mitigation did not change classification accuracy, but it consistently moved measured probabilities closer to ideal statevector outputs.

Probability-level metrics therefore revealed an improvement that hard-label accuracy alone would hide.

### Noisy accuracy requires statistical context

A single noisy simulation produced 80.0% accuracy compared with 77.5% ideal accuracy.

Repeated-seed analysis showed that noisy accuracy varied between 75.0% and 82.5%.

The apparent single-run improvement is therefore consistent with finite-shot variability and should not be interpreted as a general benefit of noise.

### Architecture advantage depends on circuit structure

Processor A and Processor B performed equally well for the classifier's chain interaction pattern.

The cyclic stress test, however, exposed a significant routing difference.

Processor B's connectivity supported the cyclic workload without additional CX gates, while Processor A required three extra CX gates and greater depth.

Therefore, processor quality cannot be inferred from qubit count alone. The relationship between logical circuit connectivity and physical processor connectivity is critical.

---

## 12. Reproducibility

The repository contains:

* deterministic dataset generation
* processor configuration JSON files
* VQC construction and training code
* transpilation utilities
* synthetic noise implementation
* readout mitigation
* repeated-seed evaluation
* architecture stress testing
* generated result tables
* generated figures
* `main.ipynb` for end-to-end presentation

The primary tested environment uses:

* Python 3.12
* Qiskit 2.5.2
* Qiskit Aer 0.17.2

Detailed package versions are provided in `requirements.txt`.

---

## 13. Conclusion

QuantumShield demonstrates an end-to-end approach to evaluating quantum classification under processor constraints and synthetic noise.

The trained 4-qubit VQC achieved 77.5% ideal test accuracy. Under repeated noisy simulation, mean classification accuracy was 79.0% with measurable finite-shot variability.

Readout mitigation did not alter hard-label accuracy but reduced mean probability MAE relative to ideal predictions by approximately 34.6% across five simulator seeds.

Processor comparisons further showed that connectivity advantages depend on workload structure. Both processors handled the classifier's chain interaction efficiently, while Processor B eliminated the additional CX routing overhead observed on Processor A for a cyclic interaction workload.

The central result is that reliable quantum-classifier evaluation requires considering probability fidelity, sampling variability, error mitigation, circuit routing, and processor connectivity together rather than relying on classification accuracy or qubit count alone.
