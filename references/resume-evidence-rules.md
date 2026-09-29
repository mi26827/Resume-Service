# Evidence and resume rules

## Claim categories

- `PROJECT_CAPABILITY`: implemented by the project; candidate authorship unproven.
- `PERSONAL_CONTRIBUTION`: candidate ownership reasonably supported.
- `EXPLORATION`: candidate research, refactor, or extension outside proven production history.

## Evidence levels

Score every claim on the independent Implementation Evidence and Attribution Evidence axes in [evidence-model.md](evidence-model.md). Only claims with at least `MEDIUM` on **both** axes enter personal bullets. User statements must be labeled and checked against code where possible. Merge commits, generated files, formatting changes, bulk renames, vendored code, and blame after refactors require extra caution.

## Git procedure

Identify authors with `git shortlog -sne --all`; match only user-confirmed identities. Use path-scoped `git log --follow`, `git show --stat` and `git show`, commit-range diffs, and targeted `git blame -L`. Review tests/config and callers, not only the changed symbol. Record hash and caveats.

When `candidate_time_window` is provided, prioritize time-bounded Git history and commit searches (conceptually, `git log --since=... --until=...`). Treat the window as the attribution scope for the current career experience, not proof that commits outside it belong to someone else. Do not count an out-of-window commit toward the current experience by default; if a `PERSONAL_CONTRIBUTION` relies on one at the user's explicit request, record the Candidate Time Window and explain why that commit was included in the evidence report.

## Bullet guardrails

Use business context + candidate action + implementation + supported value. Value may be qualitative (for example, enforces idempotent handling) when evidence shows mechanism. Metrics require a named artifact/source. Never turn team/project capability into “I built,” or an exploration proposal into “shipped to production.”
