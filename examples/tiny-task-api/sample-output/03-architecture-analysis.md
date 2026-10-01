# Architecture Analysis

> Contract: `career-miner/0.2`
> Mode: `DISCOVERY`
> Revision: `NOT_AVAILABLE`
> Status: `COMPLETE`

## Request path

1. `app.py` imports the WSGI application and starts Python's standard-library server on loopback (`app.py:1-9`).
2. `tasks/api.py` dispatches by path and method. `GET /tasks` reads the service list; `POST /tasks` reads the request body, parses JSON, and handles invalid payloads (`tasks/api.py:18-39`).
3. The handler passes the title to `TaskService.create`; the service validates and trims it, assigns an ID, and appends it to an in-memory list (`tasks/api.py:35-39`, `tasks/service.py:7-14`).
4. The API encodes response bodies as JSON and sets content type and length headers (`tasks/api.py:7-14`).

## Design observations

- The API/service boundary keeps HTTP parsing and response handling separate from task validation and storage (`tasks/api.py:18-39`, `tasks/service.py:1-14`).
- In-memory storage keeps this teaching example small, but it is volatile and local to one process (`tasks/service.py:1-14`). A database, durability, concurrent-write behavior, and production deployment are outside the evidence in this repository.
- The code shows request validation and ordinary HTTP error responses; it does not establish authentication, authorization, observability, or performance characteristics (`tasks/api.py:18-39`).

## Classification

This is a single-process WSGI teaching application. No multi-service deployment or distributed-system behavior is evidenced.
