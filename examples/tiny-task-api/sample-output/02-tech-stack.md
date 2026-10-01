# Technology Stack

> Contract: `career-miner/0.2`
> Mode: `DISCOVERY`
> Revision: `NOT_AVAILABLE`
> Status: `COMPLETE`

## Detected and used

| Technology | Role | Evidence |
|---|---|---|
| Python | Application language and runtime | `app.py:1-9`, `tasks/api.py:1-39`, `tasks/service.py:1-14` |
| WSGI / `wsgiref.simple_server` | Standard-library HTTP server and application interface | `app.py:1-9`, `tasks/api.py:11-39` |
| Standard-library `json` | Request parsing and JSON response serialization | `tasks/api.py:1-9`, `tasks/api.py:29-39` |

## Technical judgment

The request handler is wired to a small service object, and the example needs no third-party package to run. Task records are stored in a Python list inside the process (`tasks/api.py:4`, `tasks/service.py:1-14`). State is therefore lost when the process stops; the code does not show durable storage, cross-process coordination, or a production deployment. No database or performance claims are made.
