# Output contract 0.2

## Analysis modes

Choose one primary mode. `CUSTOM` is allowed only when the user explicitly selects reports.

| Mode | Required reports in addition to `SUMMARY.md` |
|---|---|
| `DISCOVERY` | `01-project-overview.md`, `02-tech-stack.md`, `03-architecture-analysis.md` |
| `CONTRIBUTION` | `04-contribution-evidence.md`, `05-backend-engineering-analysis.md` |
| `AI_AGENT` | `07-ai-agent-scan.md`, `08-agent-opportunity.md` |
| `RESUME` | `06-resume-bullets.md`, `09-interview-preparation.md` |
| `FULL` | `01` through `09` |
| `CUSTOM` | Only explicitly requested numbered reports |

Dependencies may be analyzed internally without emitting their reports. For example, `CONTRIBUTION` may perform lightweight discovery, and `RESUME` may read an existing `04-contribution-evidence.md` or re-verify necessary evidence without emitting `01`–`05`. Do not silently widen the output set. If Contribution Evidence needed by `RESUME` is unavailable, mark the run `PARTIAL` or `BLOCKED`, name the missing evidence, and do not fabricate it. On rerun, write into a new run directory or remove stale numbered files so they cannot be mistaken for current output.

## Evidence funnel and resume derivation

The logical stage order is `Source -> DISCOVERY -> CONTRIBUTION -> RESUME`, even when a narrow mode performs prerequisite checks internally. Information may move forward only after meeting the preceding stage's admission rules:

1. `DISCOVERY` establishes project purpose, technologies actually used, and architecture/runtime paths.
2. `CONTRIBUTION` establishes candidate work by pairing Implementation Evidence with independent Attribution Evidence.
3. `RESUME` converts qualifying personal claims into atomic Engineering Findings, clusters related findings, adds evidence-backed project context, and then writes the final project experience.

The resume report must make this derivation visible. It contains, in order: `Engineering Findings`, `Finding Clusters`, `Project Introduction`, `Technology Stack`, `Architecture Design Highlights`, and `Final Project Experience`. Project framing may use `PROJECT_CAPABILITY`, but final bullets may use only qualifying `PERSONAL_CONTRIBUTION`. Every final bullet lists its supporting Claim IDs; grouping does not raise or average evidence levels.

## Required header

Start every report with these machine-checkable lines after its title:

```markdown
> Contract: `career-miner/0.2`
> Mode: `FULL`
> Revision: `<commit-or-NOT_AVAILABLE>`
> Status: `COMPLETE` <!-- or PARTIAL / BLOCKED -->
```

Use the same contract, mode, revision, and status in all files from one run. `PARTIAL` names missing evidence or scope; `BLOCKED` names the blocker. An empty section is not evidence.

## Consistency rules

- Use only the category enum and evidence levels defined in [evidence-model.md](evidence-model.md).
- Keep claim IDs stable and reuse them in summary, evidence, resume, and interview reports.
- Cite repository evidence as `path:line` or `path:start-end`; cite Git evidence with a commit hash and path.
- Label external/user facts by source type and do not present them as repository-derived facts.
- Link only generated files. Do not claim missing reports were produced.
- Use `NOT_APPLICABLE` rather than invented content.
- Give every uncertainty a consequence: omitted claim, lower level, or follow-up evidence needed.

## Repeat runs

Treat the analyzed revision as an immutable snapshot. For a later run, compare claim IDs and report `ADDED`, `CHANGED`, `UNCHANGED`, or `REMOVED` only when both revisions are available. Re-evaluate levels from the new snapshot; do not carry authorship, metrics, or runtime status forward without evidence.

## Structural validation

Run the validator from the Skill repository after generating reports:

```bash
python3 scripts/validate_output.py <output-dir>
```

For a `CUSTOM` run, pass the exact numbered report filenames explicitly selected by the user. `SUMMARY.md` is always required and is not included in this list:

```bash
python3 scripts/validate_output.py <output-dir> \
  --custom-reports 01-project-overview.md 03-architecture-analysis.md
```

The validator checks supported contract headers, shared contract/mode/revision/status, required report filenames, stale numbered reports, and a few required structural sections and markers. It does not establish whether repository claims are factually correct, whether a cited author is the user, whether citations point to real lines, or whether a resume claim is truthful. Those checks require evidence review beyond this structural validator.

## Optional presentation exports

An explicitly requested technology learning guide may be drafted under `<output-path>/exports/` after `DISCOVERY` or `FULL` analysis. Present the editable Markdown draft for user review and wait for approval before creating JSON, HTML, or PDF. Approved exports are learning artifacts, not numbered reports; they do not change the required report set or contract header. See [project-learning-pdf.md](project-learning-pdf.md) for the review flow, content boundaries, schema, and rendering instructions.
