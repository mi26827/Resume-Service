# Evidence and resume rules

## Claim categories

- `PROJECT_CAPABILITY`: implemented by the project; candidate authorship unproven.
- `PERSONAL_CONTRIBUTION`: candidate ownership reasonably supported.
- `EXPLORATION`: candidate research, refactor, or extension outside proven production history.

## Evidence levels

- `STRONG`: matching candidate identity, substantive commit/diff, and live code path (ideally tests/config too).
- `MEDIUM`: code plus specific user evidence or strong corroboration, but incomplete Git attribution.
- `WEAK`: project capability exists without candidate ownership.
- `UNKNOWN`: insufficient or conflicting evidence.

Only STRONG/MEDIUM claims enter personal bullets. User statements must be labeled and checked against code where possible. Merge commits, generated files, formatting changes, bulk renames, vendored code, and blame after refactors require extra caution.

## Git procedure

Identify authors with `git shortlog -sne --all`; match only user-confirmed identities. Use path-scoped `git log --follow`, `git show --stat` and `git show`, commit-range diffs, and targeted `git blame -L`. Review tests/config and callers, not only the changed symbol. Record hash and caveats.

## Bullet guardrails

Use business context + candidate action + implementation + supported value. Value may be qualitative (for example, enforces idempotent handling) when evidence shows mechanism. Metrics require a named artifact/source. Never turn team/project capability into “I built,” or an exploration proposal into “shipped to production.”
