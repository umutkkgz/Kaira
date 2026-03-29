# KAIRA: A Control-Theoretic Framework for Stabilizing Stochastic Intelligence

**Reference implementation for the KAIRA Cognitive Control Architecture.** 

This repository contains the core logic, ontological structures, and evaluation scripts to reproduce the findings reported in our paper: *[arXiv Link Pending]*.

KAIRA (Knowledge Augmented Intelligent Rational Agent) approaches Large Language Model (LLM) hallucination not as a training deficiency, but as a bounded control problem. It introduces Meaning-Driven Reinforcement Learning (MDRL) and an Internal Deliberation Loop (IDL) to enforce strict, inference-time structural reliability over stochastic generation.

## Abstract
Large Language Models produce fluent text but remain structurally unreliable. In safety-critical deployments, this unreliability is a hard barrier. We present KAIRA, an architecture that reframes hallucination as an inference-time control instability. By substituting scalar utility rewards with a graph-topological meaning function $\mathcal{M}_{graph}(s,a)$ acting as a constraint projection operator, KAIRA ensures responses adhere strictly to an ontological boundary. The architecture includes an Epistemic Control Layer enabling the system to estimate its own competence, facilitating principled refusal under uncertainty. 

## Repository Contents

*   **`src/`**: The core execution loop (`idl_engine.py`), Epistemic refusal logic (`epistemic_layer.py`), and the Meaning subscores ($\mathcal{M}_{graph}$).
*   **`data/`**: Anonymized domain-specific queries (hospitality) and expert-annotated hallucination benchmarks (`annotated_eval.csv`). Includes the labeling guidelines (`annotation_guide.md`) to ensure transparent reproduction of our OCS measurements.
*   **`eval/`**: Scripts necessary to reproduce the empirical evaluation (Table 3 and Table 4), including the Cohen's $\kappa$ inter-rater reliability calculations and bootstrap confidence intervals.
*   **`ontology_graph.db`**: A static snapshot of the Semantic Core constraint graph (71,806 nodes, 120,840 edges) required to run the local IDL projection constraint. (Download via Releases, excluded from git tree due to size).

## Reproducing the Experiments

### 1. Environment Setup
```bash
git clone https://github.com/umutkkgz/Kaira.git
cd Kaira
pip install -r requirements.txt
```

### 2. Running the IDL Validation Benchmark
To reproduce the Table 3 base architecture vs. KAIRA IDL hallucination bounds:
```bash
python eval/run_experiment.py --mode=benchmark --runs=1000 --seed=42
```

### 3. Running the Ablation Study
To isolate the impact of the Ontological Consistency Score (OCS) against Emotional (ECS) and Contextual (CRS) sub-scores:
```bash
python eval/run_experiment.py --mode=ablation
```

## Citation
If you utilize this architecture or the provided dataset in your research, please cite:
```bibtex
@article{kaira2026,
  title={KAIRA: A Control-Theoretic Framework for Stabilizing Stochastic Intelligence},
  author={Umut K. and KAIRA Research Initiative},
  journal={arXiv preprint},
  year={2026}
}
```
