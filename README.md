# KAIRA: Runtime Governance Prototype for Bounded LLM Deployment

KAIRA is a prototype runtime control stack for deploying large language models in bounded operational settings. The repository does not introduce a new foundation model. Instead, it demonstrates how an existing generator can be wrapped with epistemic gating, semantic validation, policy-constrained routing, and explicit refusal or handoff behavior.

The current repository is aligned with the paper draft in [`paper/kaira_arxiv.tex`](paper/kaira_arxiv.tex). The prototype is intentionally small and transparent: it is a toy implementation of the architectural claims, not a production system and not evidence of open-domain reliability.

## Core Positioning

KAIRA should be read as:
- a runtime governance layer
- an epistemic control prototype
- a semantic validation pipeline
- a bounded deployment scaffold for high-capability LLMs

KAIRA should not be read as:
- a new frontier model
- a claim of universal truthfulness
- a general-purpose autonomous agent
- a replacement for foundation models

## Runtime Pipeline

```text
    [User Input]
         │
         ▼
 ┌──────────────────────┐
 │  Epistemic Control   │  -> proceed / clarify / refuse / escalate
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │     Tool Router      │  -> allowed action / human approval / deny
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │    Base Generator    │  -> candidate draft
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ Internal Deliberation│
 │ + Semantic Validation│  -> Operational Meaning Score + ontology check
 └──────────┬───────────┘
            │
            ▼
      [Bounded Output]
```

## What the Demo Shows

The toy prototype demonstrates five behaviors that match the paper:
- answerability checking before commitment
- ontology-backed rejection of unsupported drafts
- policy-gated human approval for bounded workflows
- policy-constrained routing of allowed actions
- refusal or human escalation when support is insufficient

The term `Operational Meaning Score` in this repository is used only as a bounded deployment-time admissibility score. It does not imply semantic understanding in the philosophical sense.

## Repository Contents

- `run_demo.py`: runs several short scenarios showing in-domain acceptance, ontology rejection, clarification, and escalation behavior.
- `src/epistemic_layer.py`: epistemic control logic for proceed / clarify / refuse / escalate decisions.
- `src/idl_engine.py`: internal deliberation loop, routing logic, and bounded output release.
- `src/meaning_function.py`: operational meaning score and ontology-backed subscore evaluation.
- `data/mini_ontology.json`: toy bounded ontology used by the demo.
- `paper/`: current paper source, bibliography, and compiled PDF.
- `experiments/` and `eval/`: experimental scripts and notebooks from the original repository state.

## Quick Start

Run the prototype demo:

```bash
python run_demo.py
```

The demo intentionally includes:
- a valid in-domain request
- an adversarial ontology-breaking request
- an ambiguous request that triggers clarification
- a reservation request that triggers human approval
- a request that triggers human escalation

## Reproducibility

The repository contains the current paper draft and a toy implementation that mirrors the deployment logic described there. The code is useful as an architectural reference and discussion artifact. It is not a full reproduction of a production deployment stack.

## Citation

If you reference this prototype, cite the accompanying paper in `paper/`.
