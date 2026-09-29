# Two-dimensional evidence model

Score the existence of an implementation separately from candidate ownership. Never average the scores and never use one as a proxy for the other.

## Implementation Evidence

Answers: **Does this capability exist and work in this project?**

| Level | Required interpretation |
|---|---|
| `STRONG` | Clear implementation plus corroborating runtime wiring/call chain, tests, configuration, or operational artifact. |
| `MEDIUM` | Clear implementation, but the runtime path or some wiring is incomplete or unverified. |
| `WEAK` | Only a dependency, interface, configuration fragment, comment, stub, or isolated symbol exists. |
| `UNKNOWN` | Evidence is missing, inaccessible, or conflicting. |

## Attribution Evidence

Answers: **Did the candidate implement or substantively contribute to this capability?**

| Level | Required interpretation |
|---|---|
| `STRONG` | User-confirmed Git identity, substantive commit/diff, and correspondence to the real code path. |
| `MEDIUM` | Code strongly matches a specific user statement but Git attribution is incomplete, or history is materially obscured by squash, migration, or author rewriting. State the caveat. |
| `WEAK` | The candidate changed nearby code, but substantive ownership of the claimed capability cannot be established. |
| `UNKNOWN` | No confirmed identity, relevant history, or reliable ownership evidence; evidence may also conflict. |

`USER_STATEMENT` is an evidence source, not a level. Preserve the statement and whether code corroborates it.

## Claim admission rules

| Output use | Implementation | Attribution | Category |
|---|---|---|---|
| Project capability | `MEDIUM` or `STRONG` | any | `PROJECT_CAPABILITY` |
| Personal resume bullet | `MEDIUM` or `STRONG` | `MEDIUM` or `STRONG` | `PERSONAL_CONTRIBUTION` |
| Proposal or hypothesis | any, including absent | not applicable/`UNKNOWN` | `EXPLORATION` |

A `WEAK` implementation may be reported only as a lead or gap, not as an implemented capability. A `WEAK` attribution must not use first-person ownership wording.

## Ledger schema

Use one row per atomic claim. Do not bundle independently scored capabilities.

| Field | Rule |
|---|---|
| Claim ID | Stable within a repository, for example `CAP-auth-refresh-01`; retain it across later runs when semantics are unchanged. |
| Category | Exactly one of `PROJECT_CAPABILITY`, `PERSONAL_CONTRIBUTION`, `EXPLORATION`. |
| Implementation Evidence | One of the four levels, with rationale. |
| Attribution Evidence | One of the four levels, with rationale; normally `UNKNOWN` for capability-only mode. |
| Sources | Evidence type plus repository-relative `path:line`, symbol, and commit where relevant. |
| Corroboration | Caller, test, wiring, config, user statement, or operational artifact. |
| Caveat | Missing path, conflicting evidence, generated code, history limitation, or other uncertainty. |

Downgrade rather than rationalize when sources conflict. Record what additional artifact would change the score.
