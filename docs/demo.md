# Demo

Run:

```bash
python3 run_demo.py
```

Single-prompt mode:

```bash
python3 run_demo.py --prompt "What time does the gym open?"
```

Interactive mode:

```bash
python3 run_demo.py --interactive
```

Benchmark mode:

```bash
python3 run_demo.py --benchmark
```

The script prints a compact runtime profile and then executes five scenarios:

1. accepted in-domain answer
2. ontology-boundary rejection
3. clarification request
4. approval-required reservation workflow
5. out-of-domain escalation

The goal is not to simulate a production backend. The goal is to make control flow visible to a human reviewer.
