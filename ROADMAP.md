# Roadmap

These are separate follow-up features, ordered by priority. None is implemented in this change.

## P1 — Review contribution claims with the user

Add a step where the user can confirm, edit, or exclude each proposed contribution claim before resume material is generated. Keep the original evidence and record what the user changed; user confirmation must not be treated as repository or Git evidence by itself.

## P2 — Match a job description to admitted claims

Allow a supplied job description (JD) to affect relevance and ordering only after a claim passes the existing evidence admission rules. Matching may explain why a supported claim is relevant, but must not raise its evidence level or add facts.

## P3 — Machine-readable evidence ledger and run comparison

Provide a machine-readable form of the evidence ledger and compare separate runs where both analyzed revisions are available. Preserve claim IDs, evidence dimensions, citations, uncertainty, and removal/change history.

## P4 — Analysis profiles for adjacent repository types

Add independently selectable profiles for frontend, data engineering, and infrastructure repositories. Each profile should define relevant evidence paths and questions while retaining the same attribution and claim-admission safeguards.

## Guardrails for every extension

- No feature may lower the current evidence thresholds or treat implementation evidence as authorship.
- Project capability must never be rewritten as personal contribution without independent attribution evidence.
- JD keywords must never cause project facts, experience, metrics, or claims to be invented.
- Proposed or planned work must remain clearly labeled as exploration, not completed production work.
