# backend-repo-career-miner

An evidence-first Codex Skill that turns a backend repository into architecture notes, candidate-attributed contribution evidence, truthful resume bullets, interview preparation, and—only when justified—a bounded Agent MVP proposal.

## Safety and authorization

Use this Skill only on repositories you are authorized to analyze. Analysis is **Local Only by default**: do not upload private source code to public services. Generated reports must not reproduce source files, secrets, API keys, tokens, passwords, credentials, database passwords/connection strings, or internal domains. A public GitHub repository for this Skill must contain only the Skill, generic documentation/templates/scripts, and sanitized demos—never company source code.

## Install

Copy this repository directory to your Codex skills directory, for example:

```bash
git clone https://github.com/mi26827/Resume-Service.git
cp -R Resume-Service "${CODEX_HOME:-$HOME/.codex}/skills/backend-repo-career-miner"
```

The repository name (`Resume-Service`) and Skill name (`backend-repo-career-miner`) currently differ.

## Use

Ask Codex to use `$backend-repo-career-miner` on a local backend repository. Provide the repository path and, for contribution attribution, your Git author name/email. If no mode is specified, the Skill uses `DISCOVERY`. Output defaults to `career-miner-output/`.

### Discovery

```text
Use $backend-repo-career-miner on the current repository.

Mode: DISCOVERY
```

### Contribution

```text
Use $backend-repo-career-miner in CONTRIBUTION mode.

Candidate Git identity:
Jane Doe <jane@example.com>

Candidate time window:
2026-06-01 to 2026-09-30
```

### AI / Agent

```text
Use $backend-repo-career-miner in AI_AGENT mode.

Evaluate whether this project has existing AI capabilities
and whether a real Agent opportunity exists.

Do not force an Agent.
```

### Resume

```text
Use $backend-repo-career-miner in RESUME mode.

Target role:
Backend Engineer

Experience level:
Intern

Resume language:
Chinese
```

### Full

```text
Use $backend-repo-career-miner in FULL mode for a complete analysis.
```

`FULL` should normally be used after project understanding and candidate attribution have been reviewed, and it must be explicitly requested.

The Skill is language- and framework-neutral. Its detection guide includes Java/Kotlin, Go, Python, Node.js, Rust, C#, Ruby, and PHP, while analysis follows generic backend boundaries rather than language syntax.

## Output and evidence semantics

Contract 0.2 supports `DISCOVERY`, `CONTRIBUTION`, `AI_AGENT`, `RESUME`, `FULL`, and explicitly selected `CUSTOM` output modes. The mode matrix is:

| Mode | Reports in addition to `SUMMARY.md` |
|---|---|
| `DISCOVERY` | `01`, `02`, `03` |
| `CONTRIBUTION` | `04`, `05` |
| `AI_AGENT` | `07`, `08` |
| `RESUME` | `06`, `09` |
| `FULL` | `01` through `09` |
| `CUSTOM` | Explicitly requested reports |

It generates only mode-relevant reports and separates:

- `PROJECT_CAPABILITY`: present in the project but not proven as the candidate's work.
- `PERSONAL_CONTRIBUTION`: supported by STRONG or MEDIUM attribution evidence.
- `EXPLORATION`: proposed research, refactoring, or AI/Agent extension—not claimed as production work.

No performance or scale metric is emitted without an explicit benchmark, monitoring artifact, test result, or authorized user-supplied source.

Every claim has two independent scores: **Implementation Evidence** says whether the capability exists and is wired; **Attribution Evidence** says whether the candidate substantively contributed it. An Agent is recommended only after workflow, judgment, tool-loop, evaluation, and safety gates pass; deterministic automation or no solution are valid outcomes.

Resume generation follows a one-way evidence funnel rather than drafting claims first: source code establishes the project, stack, and architecture; Git analysis identifies the candidate's work with two-dimensional evidence; qualifying claims become atomic engineering findings; related findings are clustered; and only then are the project introduction, stack, architecture highlights, and final project experience written. The final bullets retain Claim IDs so they can be traced back to both implementation and attribution evidence.

## License

Apache License 2.0. See [LICENSE](LICENSE).
