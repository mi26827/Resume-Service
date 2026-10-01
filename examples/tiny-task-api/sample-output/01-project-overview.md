# Project Overview

> Contract: `career-miner/0.2`
> Mode: `DISCOVERY`
> Revision: `NOT_AVAILABLE`
> Status: `COMPLETE`

## Purpose

This synthetic teaching project exposes a small HTTP API for listing and creating tasks. The local entry point starts a WSGI server on `127.0.0.1:8000` (`app.py:1-9`).

## Observed capabilities

- `PROJECT_CAPABILITY`: `GET /tasks` returns the current task list, while `POST /tasks` parses a JSON object and returns a created task (`tasks/api.py:18-39`).
- `PROJECT_CAPABILITY`: task creation rejects a missing, non-string, or blank title, trims accepted titles, assigns a sequential in-process ID, and stores a copy in the service list (`tasks/service.py:1-14`).

## Scope and limits

The service keeps state in memory and has no database or persistence layer (`tasks/service.py:1-14`). This small example does not establish production readiness, deployment, performance, or business impact. No candidate contribution is assessed in `DISCOVERY` mode.
