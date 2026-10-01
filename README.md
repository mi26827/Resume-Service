# backend-repo-career-miner

[中文说明](README.zh-CN.md)

`Resume-Service` is the name of this Git repository. `backend-repo-career-miner` is the name of the Codex Skill inside it. Despite the repository name, this project is **not** an online resume website, a resume-hosting service, or a backend service. It is a prompt-and-reference package that helps Codex analyze an authorized local code repository and produce evidence-based career notes.

## Who it is for

Use the Skill if you are a student, job seeker, or software engineer who wants to understand a backend codebase, review your own Git-backed work, prepare for interviews, or draft resume material from verifiable engineering evidence. It is language- and framework-neutral, with stack guidance for Java/Kotlin, Go, Python, Node.js, Rust, C#, Ruby, and PHP.

The analysis input is a local repository path. `DISCOVERY` needs no candidate identity. To analyze personal contributions, provide and confirm the Git author name and/or email that identifies your commits. Without user-confirmed identity information, the Skill must not guess which commits belong to you; it can still describe project capabilities without attributing them to a person.

## Install

Clone this Skill repository, then copy it into your Codex skills directory:

```bash
git clone https://github.com/mi26827/Resume-Service.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R Resume-Service "${CODEX_HOME:-$HOME/.codex}/skills/backend-repo-career-miner"
```

If Codex does not recognize the Skill yet, reload or restart Codex. The install directory uses the Skill name, even though the source repository is named `Resume-Service`.

## Quick start: first DISCOVERY report

Choose a local backend repository you are authorized to inspect. In Codex, ask:

```text
Use $backend-repo-career-miner to analyze this repository:
<absolute path to the local backend repository>

Mode: DISCOVERY
```

The Skill writes reports to `career-miner-output/` inside the target repository by default. Discovery produces `SUMMARY.md`, `01-project-overview.md`, `02-tech-stack.md`, and `03-architecture-analysis.md`. You can inspect the files locally as soon as the run finishes.

For a tiny teaching example with a checked-in sample report, see [`examples/tiny-task-api/README.md`](examples/tiny-task-api/README.md). It is entirely synthetic and is not a production case.

## Choose a mode

Every run includes `SUMMARY.md`. Standard modes emit exactly these numbered reports:

| Mode | Use it for | Numbered reports |
|---|---|---|
| `DISCOVERY` | Project purpose, technologies in use, and architecture | `01`–`03` |
| `CONTRIBUTION` | Git-backed candidate contribution and backend engineering analysis | `04`–`05` |
| `AI_AGENT` | Existing AI capabilities and whether an Agent opportunity is justified | `07`–`08` |
| `RESUME` | Evidence-backed resume bullets and interview preparation | `06`, `09` |
| `FULL` | All analysis areas in one run | `01`–`09` |
| `CUSTOM` | A user-selected report subset | Explicitly selected reports only |

The default is `DISCOVERY`. `FULL` runs across all areas and must be explicitly requested. A narrow mode may analyze prerequisite information internally, but it does not silently add unrelated reports to the output.

Example requests for the other modes:

```text
Use $backend-repo-career-miner in AI_AGENT mode on <local repository path>.
Check existing AI capabilities and whether a real Agent opportunity exists.
Do not force an Agent.
```

```text
Use $backend-repo-career-miner in RESUME mode on <local repository path>.
Target role: Backend Engineer
Experience level: Intern
Resume language: Chinese
```

```text
Use $backend-repo-career-miner in FULL mode on <local repository path>.
```

Only the last request selects `FULL`; the Skill must not infer it. `CUSTOM` requests should name the exact numbered reports to emit.

For contribution analysis, include a confirmed identity in your request, for example:

```text
Use $backend-repo-career-miner in CONTRIBUTION mode on <local repository path>.

Candidate Git identity (confirmed by me):
<author name> and/or <author email>
```

You may also give a candidate time window. If you do not provide confirmed identity information, authorship remains unknown and no personal contribution should be claimed. Source code shows what a project can do; it does not show who wrote it.

## Evidence and privacy boundaries

The Skill reads the target repository from the local filesystem and writes reports to the selected local output directory. This repository contains no source uploader or telemetry. Codex still processes the material needed for analysis according to the user's configured Codex runtime and data-handling settings; check those settings before analyzing restricted repositories. Use the Skill only on repositories you are authorized to inspect, and do not ask it to publish private code. Generated reports must not reproduce secrets, credentials, internal domains, or source files wholesale.

The output keeps three kinds of statements separate:

- `PROJECT_CAPABILITY`: something present in the project, with implementation evidence.
- `PERSONAL_CONTRIBUTION`: work attributed to the candidate only with independent Git attribution evidence. Implementation evidence alone is not authorship.
- `EXPLORATION`: a possible future investigation or design, not completed project work.

Every claim tracks two independent dimensions: **Implementation Evidence** establishes whether a capability exists and is wired; **Attribution Evidence** establishes whether the candidate substantively contributed it. Resume claims pass through an evidence funnel: project understanding, candidate attribution, atomic engineering findings, grouping, and then final project experience. Unsupported performance or scale metrics are not invented. An Agent proposal is optional and requires a supported workflow with meaningful judgment, tool use, evaluation, and safety boundaries; deterministic automation or no suitable opportunity are valid conclusions. Target role, experience level, and resume language can shape presentation, not project facts or evidence levels.

## Output contract and validation

Contract 0.2 defines each mode's output set in [`references/output-contract.md`](references/output-contract.md). To check generated output from this repository:

```bash
python3 scripts/validate_output.py <output-dir>
```

For `CUSTOM`, pass the exact report filenames the user selected (without `SUMMARY.md`):

```bash
python3 scripts/validate_output.py <output-dir> \
  --custom-reports 01-project-overview.md 03-architecture-analysis.md
```

The validator checks headers, report-set consistency, and selected structural requirements. Passing it is not proof that claims are factual, that Git identity is correct, that citations are valid, or that resume content is truthful; those require evidence review.

## License

Apache License 2.0. See [LICENSE](LICENSE).
