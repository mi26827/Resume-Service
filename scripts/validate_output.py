#!/usr/bin/env python3
"""Validate the stable, machine-checkable parts of career-miner contract 0.2."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPORTS = {
    "01-project-overview.md",
    "02-tech-stack.md",
    "03-architecture-analysis.md",
    "04-contribution-evidence.md",
    "05-backend-engineering-analysis.md",
    "06-resume-bullets.md",
    "07-ai-agent-scan.md",
    "08-agent-opportunity.md",
    "09-interview-preparation.md",
}
MODE_REPORTS = {
    "DISCOVERY": {"01-project-overview.md", "02-tech-stack.md", "03-architecture-analysis.md"},
    "CONTRIBUTION": {"04-contribution-evidence.md", "05-backend-engineering-analysis.md"},
    "AI_AGENT": {"07-ai-agent-scan.md", "08-agent-opportunity.md"},
    "RESUME": {"06-resume-bullets.md", "09-interview-preparation.md"},
    "FULL": REPORTS,
}
HEADER = re.compile(
    r"> Contract: `career-miner/0\.2`\s*\n"
    r"> Mode: `(?P<mode>DISCOVERY|CONTRIBUTION|AI_AGENT|RESUME|FULL|CUSTOM)`\s*\n"
    r"> Revision: `(?P<revision>[^`]+)`\s*\n"
    r"> Status: `(?P<status>COMPLETE|PARTIAL|BLOCKED)`"
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"output directory does not exist: {root}"]
    files = {path.name for path in root.glob("*.md")}
    if "SUMMARY.md" not in files:
        errors.append("missing required SUMMARY.md")
    generated = files & REPORTS
    metadata: dict[str, tuple[str, str]] = {}
    for name in sorted(generated | ({"SUMMARY.md"} & files)):
        text = (root / name).read_text(encoding="utf-8")
        match = HEADER.search(text)
        if not match:
            errors.append(f"{name}: missing or invalid contract header")
            continue
        metadata[name] = (match.group("mode"), match.group("revision"))
    run_values = set(metadata.values())
    if len(run_values) > 1:
        errors.append("reports do not share one mode and revision")
    if run_values:
        mode, _ = next(iter(run_values))
        if mode in MODE_REPORTS:
            missing = MODE_REPORTS[mode] - generated
            extra = generated - MODE_REPORTS[mode]
            if missing:
                errors.append(f"{mode}: missing reports: {', '.join(sorted(missing))}")
            if extra:
                errors.append(f"{mode}: stale or unexpected reports: {', '.join(sorted(extra))}")
    contribution_files = generated & {"04-contribution-evidence.md", "06-resume-bullets.md"}
    for name in sorted(contribution_files):
        text = (root / name).read_text(encoding="utf-8")
        if "Implementation Evidence" not in text or "Attribution Evidence" not in text:
            errors.append(f"{name}: both evidence dimensions are required")
    if "06-resume-bullets.md" in generated:
        text = (root / "06-resume-bullets.md").read_text(encoding="utf-8")
        required_sections = (
            "Engineering Findings",
            "Finding Clusters",
            "Project Introduction",
            "Technology Stack",
            "Architecture Design Highlights",
            "Final Project Experience",
        )
        missing_sections = [
            section for section in required_sections if f"## {section}" not in text
        ]
        if missing_sections:
            errors.append(
                "06-resume-bullets.md: missing evidence-funnel sections: "
                + ", ".join(missing_sections)
            )
    if "08-agent-opportunity.md" in generated:
        text = (root / "08-agent-opportunity.md").read_text(encoding="utf-8")
        outcomes = re.findall(
            r"(?m)^- Outcome:\s*`(PROPOSE_AGENT|RECOMMEND_DETERMINISTIC_AUTOMATION|NO_SUITABLE_OPPORTUNITY|INSUFFICIENT_EVIDENCE)`\s*$",
            text,
        )
        if len(outcomes) != 1:
            errors.append("08-agent-opportunity.md: exactly one concrete Outcome is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    errors = validate(args.output_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("career-miner output conforms to contract 0.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
