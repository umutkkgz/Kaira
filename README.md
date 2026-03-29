# Meaning-Driven AI Control: Reference Implementation of the KAIRA Architecture

KAIRA introduces a Meaning-Driven Control Layer for stabilizing large language model reasoning.

This repository serves as the empirical testbed and reference artifact for the control-theoretic framework detailed in our preprint *[arXiv Link Pending]*. We propose that intelligence stabilization requires separating probabilistic generation from deterministic, graph-topological boundary validation.

**Field Claim:** This work advances the field of *Meaning-Driven AI Control*, establishing that hallucination is an inference-time control instability, not a model scaling deficiency.

## Architecture Pipeline

```text
    [User Input]
         │
         ▼
 ┌───────────────┐
 │   Base LLM    │ (Stochastic Generation)
 └───────┬───────┘
         │ Candidate Draft (a)
         ▼
 ┌───────────────┐
 │      IDL      │ (Internal Deliberation Loop)
 │ ┌───────────┐ │
 │ │ SAS (Sim) │ │ 
 │ │ ECS (Emo) │ │
 │ │ CRS (Ctx) │ │
 │ │ OCS (Ont) │ │
 │ └─────┬─────┘ │
 └───────┼───────┘
         │ M(s,a) Energy Score
         ▼
 ┌───────────────┐
 │Epistemic Gate │ (Refusal / Competence Estimator)
 └───────┬───────┘
         │ Validation Passed
         ▼
   [Safe Output]
```

## Abstract
Large Language Models produce fluent text but remain structurally unreliable. In safety-critical deployments, this unreliability is a hard barrier. We present KAIRA, an architecture that reframes hallucination as an inference-time control instability. By substituting scalar utility rewards with a graph-topological meaning function $\mathcal{M}_{graph}(s,a)$ acting as a constraint projection operator, KAIRA ensures responses adhere strictly to an ontological boundary. The architecture includes an Epistemic Control Layer enabling the system to estimate its own competence, facilitating principled refusal under uncertainty. 

## Repository Contents

*   **`run_demo.py`**: A transparent script exposing the internal reflection, measurement, and epistemic gating of a simulated generation. Let the code speak.
*   **`src/`**: The core execution loop (`idl_engine.py`), Epistemic refusal logic (`epistemic_layer.py`), and the Meaning subscores ($\mathcal{M}_{graph}$).
*   **`experiments/`**: Scripts and data reproducing the empirical claims.
    *   `annotated_eval.csv`: Empirical hallucination labels derived from 1,200 samples.
    *   `run_experiment.py`: Main driver to replicate Table 3 (Bounds) and Table 4 (Ablation).
    *   `ablation_study.ipynb`: Cell-by-cell inspection of the OCS ablation failure cascade.
    *   `annotation_guide.md`: Strict academic guidelines defining our hallucination evaluations.

## Reproducibility 

### 1. Architectural Trace Demo
See the internal control mechanisms in action instantly:
```bash
python run_demo.py
```

### 2. Full Experiment Benchmark via Docker (Recommended)
You can recreate our statistical proofs seamlessly:
```bash
docker compose up kaira-eval
```
```bash
docker compose up kaira-ablation
```

## Citation
If you build upon this architecture or utilize the dataset to advance Meaning-Driven Control, please cite:
```bibtex
@article{kaira2026,
  title={KAIRA: A Control-Theoretic Framework for Stabilizing Stochastic Intelligence},
  author={Umut K. and KAIRA Research Initiative},
  journal={arXiv preprint},
  year={2026}
}
```
