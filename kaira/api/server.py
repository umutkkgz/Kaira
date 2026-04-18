from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from kaira.core.types import UserInput
from kaira.eval.benchmarks import BenchmarkRunner
from kaira.ontology.loader import OntologyGraph
from kaira.runtime.controller import RuntimeController
from kaira.ui.dashboard import render_dashboard
from kaira.utils.config import load_config


ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY_PATH = ROOT / "data" / "mini_ontology.json"
POLICY_PATH = ROOT / "data" / "default_policy.json"
RUNTIME_PATH = ROOT / "data" / "default_runtime.json"

controller = RuntimeController(
    OntologyGraph.from_file(ONTOLOGY_PATH),
    load_config(POLICY_PATH),
    load_config(RUNTIME_PATH),
)
app = FastAPI(title="KAIRA Runtime Governance API", version="0.3.0")
TRACE_STORE: dict[str, dict] = {}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "kaira-runtime"}


@app.get("/policy")
def policy() -> dict:
    return load_config(POLICY_PATH)


@app.get("/ontology/stats")
def ontology_stats() -> dict:
    return controller.ontology.summary()


@app.post("/process")
def process(payload: dict) -> dict:
    response = controller.process(UserInput(query=payload["query"], session_id=payload.get("session_id", "api-session")))
    TRACE_STORE[response.trace.trace_id] = response.trace.to_dict()
    return {
        "text": response.text,
        "final_status": response.final_status,
        "route_action": response.route_action,
        "memory_action": response.memory_action,
        "trace": response.trace.to_dict(),
    }


@app.post("/eval/run")
def run_eval() -> dict:
    result = BenchmarkRunner(controller).export(ROOT / "eval" / "results")
    return {
        "run_id": result.run_id,
        "scenario_count": result.scenario_count,
        "metrics": result.metrics,
    }


@app.get("/benchmarks/summary")
def benchmark_summary() -> dict:
    summary_path = ROOT / "eval" / "results" / "benchmark_summary.json"
    if not summary_path.exists():
        result = BenchmarkRunner(controller).export(ROOT / "eval" / "results")
        return {
            "run_id": result.run_id,
            "scenario_count": result.scenario_count,
            "metrics": result.metrics,
        }
    return load_config(summary_path)


@app.post("/simulate")
def simulate(payload: dict) -> dict:
    response = controller.process(UserInput(query=payload["query"], session_id=payload.get("session_id", "simulate-session")))
    TRACE_STORE[response.trace.trace_id] = response.trace.to_dict()
    return {
        "simulation": True,
        "trace": response.trace.to_dict(),
        "final_text": response.text,
        "status": response.final_status,
    }


@app.get("/trace/{trace_id}")
def get_trace(trace_id: str) -> dict:
    return TRACE_STORE.get(trace_id, {"error": "trace_not_found"})


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return render_dashboard()
