# QuantumShield

**Noise-Resilient Quantum Classification & Error Mitigation**

Qiskit Fall Fest 2026 - Phase 1
Problem Statement: **PS-Q3 - Noise-Resilient Classification & Error Mitigation**

## Overview

QuantumShield is an end-to-end 4-qubit Variational Quantum Classifier (VQC) experiment that studies two practical challenges in noisy quantum machine learning:

1. How synthetic device noise affects classification outputs.
2. How processor connectivity affects transpilation and routing overhead.

The same trained VQC is evaluated on two simulated processor architectures, Processor A and Processor B, under identical synthetic noise conditions.

A readout-error mitigation method is then applied and evaluated not only through classification accuracy, but also through probability-level error relative to ideal statevector predictions.

A separate cyclic connectivity stress test is used to isolate architectural differences between the two processors.

## Key Results

| Experiment                              | Result                     |
| --------------------------------------- | -------------------------- |
| Ideal VQC test accuracy                 | **77.5%**                  |
| Mean noisy accuracy across 5 seeds      | **79.0%**                  |
| Noisy accuracy standard deviation       | **2.85 percentage points** |
| Mean noisy probability MAE              | **0.009598**               |
| Mean mitigated probability MAE          | **0.006276**               |
| Relative MAE reduction                  | **~34.6%**                 |
| Processor A cyclic stress-test depth    | **11**                     |
| Processor B cyclic stress-test depth    | **8**                      |
| Processor A cyclic stress-test CX count | **7**                      |
| Processor B cyclic stress-test CX count | **4**                      |

Readout mitigation did not change hard-label accuracy because the symmetric correction preserves the 0.5 decision threshold. However, it consistently reduced probability-level error across all five tested simulator seeds.

For the original chain-like classifier circuit, Processor A and Processor B transpiled equally efficiently. In the separate cyclic interaction stress test, Processor B required no additional CX gates, while Processor A required three additional CX gates.

This demonstrates that processor-connectivity advantages depend on the logical interaction structure of the quantum circuit.

## Experimental Setup

### Dataset

A deterministic synthetic binary-classification dataset is generated using:

```python
make_classification(
    n_samples=200,
    n_features=4,
    n_informative=3,
    n_redundant=0,
    n_classes=2,
    random_state=42
)
```

The dataset is split into:

* 160 training samples
* 40 testing samples

Features are scaled to `[0, π]` for quantum angle encoding.

### Variational Quantum Classifier

The classifier uses:

* 4 qubits
* RY angle encoding
* 8 trainable parameters
* CX entanglement
* COBYLA optimization
* binary cross-entropy objective

The model is trained once under ideal statevector simulation. The resulting parameters are frozen and reused for all processor and noise experiments.

This prevents processor-specific retraining from confounding the comparison.

## Processor Architectures

### Processor A

* 5 physical qubits
* Sparse branching/tree-style connectivity

### Processor B

* 9 physical qubits
* Sparse heavy-hex-inspired connectivity

Both processors use the native basis:

```text
rz, sx, x, cx
```

Transpilation uses:

* Optimization level: `1`
* Transpiler seed: `42`

## Synthetic Noise Model

Both processors use identical noise rates so that differences are not caused by different error strengths.

| Noise source               | Error rate |
| -------------------------- | ---------: |
| 1-qubit depolarizing error |      0.001 |
| CX depolarizing error      |      0.005 |
| Readout error              |       0.01 |

Noisy simulations use **4096 shots**.

## Error Mitigation

QuantumShield applies symmetric readout-error mitigation.

For observed class-1 probability \(p_{obs}\) and readout-error probability \(e\):

$$
p_{corrected} =
\frac{p_{obs}-e}{1-2e}
$$

with corrected probabilities clipped to `[0, 1]`.

Because this transformation preserves the 0.5 decision boundary, classification accuracy may remain unchanged even when probability estimates improve.

Therefore mitigation quality is evaluated using MAE and RMSE against exact ideal statevector probabilities.

### Single-Seed Result

For simulator seed 42:

| Metric           |    Noisy |    Mitigated |
| ---------------- | -------: | -----------: |
| Accuracy         |    80.0% |        80.0% |
| Probability MAE  | 0.007789 | **0.004656** |
| Probability RMSE | 0.009903 | **0.006018** |

### Repeated-Seed Result

Five simulator seeds were evaluated:

```text
42, 123, 256, 512, 1024
```

Across these runs:

* Mean noisy accuracy: **79.0%**
* Accuracy standard deviation: **2.85 percentage points**
* Mean noisy MAE: **0.009598**
* Mean mitigated MAE: **0.006276**
* Relative MAE reduction: **~34.6%**

Mitigation reduced probability MAE for every tested seed.

## Processor Connectivity Analysis

The trained classifier uses a simple chain-like entanglement structure. Both processor architectures can embed this interaction pattern efficiently.

Baseline classifier transpilation therefore produced the same principal routing result for both processors:

* CX count: 3
* Transpiled depth: 15
* Additional CX overhead: 0

Rather than forcing an artificial processor difference, QuantumShield reports this result directly.

A separate four-qubit cyclic interaction circuit is then used to stress processor connectivity.

### Cyclic Stress-Test Results

| Metric              | Processor A | Processor B |
| ------------------- | ----------: | ----------: |
| Logical depth       |           5 |           5 |
| Logical CX count    |           4 |           4 |
| Transpiled depth    |      **11** |       **8** |
| Transpiled CX count |       **7** |       **4** |
| CX overhead         |      **+3** |       **0** |

Processor B therefore used approximately **42.9% fewer transpiled CX gates** and achieved approximately **27.3% lower transpiled depth** than Processor A for this workload.

The reported final-basis SWAP count is zero because routing operations are decomposed into the processor's native basis. The additional CX gates on Processor A capture the relevant routing overhead.

## Main Findings

### 1. Accuracy alone is insufficient for evaluating mitigation

Readout mitigation did not change the hard classification labels, but substantially improved probability-level agreement with the ideal VQC.

### 2. Finite-shot noise can alter measured accuracy

The ideal test accuracy was 77.5%, while noisy runs varied across simulator seeds.

The noisy result should therefore not be interpreted as evidence that noise inherently improves classification.

### 3. Processor architecture matters conditionally

Processor B was not automatically superior for every circuit.

The chain-like classifier mapped efficiently to both processors, while the cyclic stress workload exposed Processor B's connectivity advantage.

### 4. Fair processor comparison requires controlled noise

Processor A and Processor B use identical synthetic noise parameters. This isolates connectivity and routing effects from device-quality differences.

## Repository Structure

```text
quantum-shield/
|
|-- README.md
|-- report.md
|-- main.ipynb
|-- main.py
|-- requirements.txt
|-- create_notebook.py
|
|-- data/
|   |-- raw/
|   `-- processed/
|
|-- processors/
|   |-- processor_A.json
|   `-- processor_B.json
|
|-- src/
|   |-- problem.py
|   |-- processors.py
|   |-- routing.py
|   |-- metrics.py
|   |-- visualization.py
|   |-- vqc.py
|   |-- classifier.py
|   |-- train_vqc.py
|   |-- noise.py
|   |-- mitigation.py
|   |-- benchmark_noise.py
|   |-- benchmark_mitigation.py
|   |-- analyze_mitigation.py
|   |-- repeated_benchmark.py
|   |-- architecture_stress.py
|   `-- create_final_figures.py
|
`-- results/
    |-- tables/
    `-- figures/
    
## Reproducing the Project

Python 3.12 was used for the tested environment.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Open the main notebook

Open:

```text
main.ipynb
```

and run all cells.

The notebook presents the saved experimental results and figures generated by the reproducible scripts in `src/`.

## Re-running Experiments

Dataset verification:

```bash
python -m src.verify_dataset
```

VQC verification:

```bash
python -m src.verify_vqc
```

Train the VQC:

```bash
python -m src.train_vqc
```

Processor routing benchmark:

```bash
python -m src.benchmark_routing
```

Noise benchmark:

```bash
python -m src.benchmark_noise
```

Readout mitigation:

```bash
python -m src.benchmark_mitigation
```

Probability-level mitigation analysis:

```bash
python -m src.analyze_mitigation
```

Repeated-seed robustness experiment:

```bash
python -m src.repeated_benchmark
```

Architecture stress test:

```bash
python -m src.architecture_stress
```

Generate final figures:

```bash
python -m src.create_final_figures
```

## Generated Results

Important quantitative outputs are stored under:

```text
results/tables/
```

Important visualizations are stored under:

```text
results/figures/
```

These include:

* processor topology diagrams
* VQC training convergence
* repeated-seed accuracy
* mitigation probability-error comparison
* architecture routing comparison

## Conclusion

QuantumShield demonstrates an end-to-end workflow for evaluating a variational quantum classifier under realistic synthetic noise and processor-connectivity constraints.

The experiments show that readout mitigation can improve probability fidelity even when classification accuracy is unchanged, and that processor-connectivity benefits depend on the interaction topology of the quantum workload.

Rather than treating qubit count or accuracy as sufficient indicators of performance, QuantumShield evaluates classification, noise, mitigation, routing, circuit depth, and connectivity together.
