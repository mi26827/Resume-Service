# backend-repo-career-miner

An evidence-first Codex Skill that turns a backend repository into architecture notes, candidate-attributed contribution evidence, truthful resume bullets, interview preparation, and—only when justified—a bounded Agent MVP proposal.

## Safety and authorization

Use this Skill only on repositories you are authorized to analyze. Analysis is **Local Only by default**: do not upload private source code to public services. Generated reports must not reproduce source files, secrets, API keys, tokens, passwords, credentials, database passwords/connection strings, or internal domains. A public GitHub repository for this Skill must contain only the Skill, generic documentation/templates/scripts, and sanitized demos—never company source code.

## Install

Copy this repository directory to your Codex skills directory, for example:

```bash
cp -R backend-repo-career-miner "${CODEX_HOME:-$HOME/.codex}/skills/backend-repo-career-miner"
```

## Use

Ask Codex to use `$backend-repo-career-miner` on a local backend repository. Provide the repository path and, for contribution attribution, your Git author name/email. The Skill first detects the real stack, follows runtime call chains, then correlates code with Git history. Output defaults to `career-miner-output/`.

Example requests:

```text
Use $backend-repo-career-miner to analyze /path/to/java-service.
My Git author is Jane Doe <jane@example.com>.
```

```text
Use $backend-repo-career-miner on /path/to/go-api, but produce capability analysis only; do not attribute authorship.
```

The Skill is language- and framework-neutral. Its detection guide includes Java/Kotlin, Go, Python, Node.js, Rust, C#, Ruby, and PHP, while analysis follows generic backend boundaries rather than language syntax.

## Output and evidence semantics

Contract 0.2 supports `FULL`, `CAPABILITY`, `ATTRIBUTION`, `RESUME`, `AI_AGENT`, and explicitly selected `CUSTOM` output modes. It generates only mode-relevant reports and separates:

- `PROJECT_CAPABILITY`: present in the project but not proven as the candidate's work.
- `PERSONAL_CONTRIBUTION`: supported by STRONG or MEDIUM attribution evidence.
- `EXPLORATION`: proposed research, refactoring, or AI/Agent extension—not claimed as production work.

No performance or scale metric is emitted without an explicit benchmark, monitoring artifact, test result, or authorized user-supplied source.

Every claim has two independent scores: **Implementation Evidence** says whether the capability exists and is wired; **Attribution Evidence** says whether the candidate substantively contributed it. An Agent is recommended only after workflow, judgment, tool-loop, evaluation, and safety gates pass; deterministic automation or no solution are valid outcomes.

## License

Apache License 2.0. See [LICENSE](LICENSE).
