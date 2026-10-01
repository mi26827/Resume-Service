# Tiny Task API (synthetic teaching example)

This is a small, fully synthetic backend repository for learning how `backend-repo-career-miner` reads implementation evidence. It is a teaching sample, not a real company project or a production case. It contains no real credentials, people, or company code.

## Run locally

Requires Python 3.10 or newer and uses only the Python standard library:

```bash
python3 app.py
```

The server listens on `127.0.0.1:8000`. In another terminal, try:

```bash
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Read the sample"}'
```

Tasks are kept in process memory and disappear when the server stops. The example does not claim persistence, deployment, performance, or business results.

The repository's unit suite also exercises the WSGI app directly, without opening a port. Run it from the Skill repository root with `python -m unittest discover -v`; the cases are in [`tests/test_tiny_task_api.py`](../../tests/test_tiny_task_api.py).

## Analyze it with the Skill

In Codex, ask it to analyze the absolute path to this directory:

```text
Use $backend-repo-career-miner to analyze <absolute path to examples/tiny-task-api>.

Mode: DISCOVERY
```

The Skill writes its run to `career-miner-output/` in this example repository. [`sample-output/`](sample-output/SUMMARY.md) is a separate, concise reference DISCOVERY run. Its code citations use paths and line numbers relative to this directory; compare them with `app.py` and `tasks/`.

To check the checked-in sample report from the Skill repository root, run:

```bash
python3 scripts/validate_output.py examples/tiny-task-api/sample-output
```

The validator checks report structure and metadata consistency. It does not prove that claims or authorship are true; the sample makes no candidate-contribution claims.
