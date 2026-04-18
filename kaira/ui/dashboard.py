from __future__ import annotations


def render_dashboard() -> str:
    return """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <title>KAIRA Runtime Dashboard</title>
      <style>
        body { font-family: Helvetica, Arial, sans-serif; margin: 2rem; background: #f5f4ef; color: #1d1d1b; }
        .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
        .card { background: white; border: 1px solid #d7d1c4; border-radius: 16px; padding: 1rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04); }
        h1, h2 { margin-top: 0; }
        code { background: #f0ece3; padding: 0.2rem 0.4rem; border-radius: 6px; }
      </style>
    </head>
    <body>
      <h1>KAIRA Runtime Governance Dashboard</h1>
      <p>Demo surface for bounded LLM deployment traces, policy routing, ontology validation, and handoff outcomes.</p>
      <div class="grid">
        <div class="card">
          <h2>Runtime Pipeline</h2>
          <p><code>ECL -> Router -> IDL -> Validator -> Memory/Handoff</code></p>
        </div>
        <div class="card">
          <h2>Trace Fields</h2>
          <p>ECL score, route decision, ontology hits, OMS, validator status, final status, and latency breakdown.</p>
        </div>
        <div class="card">
          <h2>Demo Scenarios</h2>
          <p>In-domain answer, ontology rejection, clarification, approval-required route, and out-of-domain escalation.</p>
        </div>
        <div class="card">
          <h2>API Endpoints</h2>
          <p><code>POST /process</code>, <code>POST /eval/run</code>, <code>GET /policy</code>, <code>GET /ontology/stats</code></p>
        </div>
      </div>
    </body>
    </html>
    """

