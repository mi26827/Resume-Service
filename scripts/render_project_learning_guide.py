#!/usr/bin/env python3
"""Render a Career Miner project-learning JSON guide to HTML and PDF."""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "career-miner/project-learning-guide/1.0"
CHROMIUM_NAMES = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")


def _text(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")


def _string_array(value: Any, field: str, errors: list[str], *, allow_empty: bool = True) -> None:
    if not isinstance(value, list) or (not allow_empty and not value):
        errors.append(f"{field} must be an array" + ("" if allow_empty else " with at least one item"))
        return
    for index, item in enumerate(value):
        _text(item, f"{field}[{index}]", errors)


def _validate_evidence(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty array")
        return
    for index, entry in enumerate(value):
        prefix = f"{field}[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        unexpected = set(entry) - {"citation", "supports", "source_type"}
        if unexpected:
            errors.append(f"{prefix} has unexpected fields: " + ", ".join(sorted(unexpected)))
        _text(entry.get("citation"), f"{prefix}.citation", errors)
        _text(entry.get("supports"), f"{prefix}.supports", errors)
        source_type = entry.get("source_type")
        if not isinstance(source_type, str) or source_type not in {
            "REPOSITORY",
            "USER_STATEMENT",
        }:
            errors.append(f"{prefix}.source_type must be REPOSITORY or USER_STATEMENT")


def validate_document(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["the JSON root must be an object"]

    required = {
        "schema_version",
        "approval_status",
        "language",
        "project_name",
        "project_overview",
        "overview_evidence",
        "technologies",
        "flows",
        "study_questions",
    }
    allowed = required
    missing = required - set(document)
    unexpected = set(document) - allowed
    if missing:
        errors.append("missing top-level fields: " + ", ".join(sorted(missing)))
    if unexpected:
        errors.append("unexpected top-level fields: " + ", ".join(sorted(unexpected)))
    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    if document.get("approval_status") != "APPROVED":
        errors.append("approval_status must be APPROVED before PDF rendering")
    language = document.get("language")
    if not isinstance(language, str) or language not in {"zh-CN", "en-US"}:
        errors.append("language must be 'zh-CN' or 'en-US'")

    _text(document.get("project_name"), "project_name", errors)
    _text(document.get("project_overview"), "project_overview", errors)
    _validate_evidence(document.get("overview_evidence"), "overview_evidence", errors)

    technologies = document.get("technologies")
    if not isinstance(technologies, list) or not technologies:
        errors.append("technologies must be an array with at least one item")
        technologies = []
    technology_names: set[str] = set()
    for index, technology in enumerate(technologies):
        prefix = f"technologies[{index}]"
        if not isinstance(technology, dict):
            errors.append(f"{prefix} must be an object")
            continue
        required_technology_fields = {
            "name",
            "role",
            "project_usage",
            "integration",
            "learning_notes",
            "evidence",
        }
        allowed_technology_fields = required_technology_fields | {"design_considerations"}
        missing_fields = required_technology_fields - set(technology)
        unexpected_fields = set(technology) - allowed_technology_fields
        if missing_fields:
            errors.append(f"{prefix} missing fields: " + ", ".join(sorted(missing_fields)))
        if unexpected_fields:
            errors.append(f"{prefix} has unexpected fields: " + ", ".join(sorted(unexpected_fields)))
        _text(technology.get("name"), f"{prefix}.name", errors)
        if isinstance(technology.get("name"), str):
            technology_names.add(technology["name"].strip())
        for field in ("role", "project_usage", "integration"):
            _text(technology.get(field), f"{prefix}.{field}", errors)
        _string_array(technology.get("learning_notes"), f"{prefix}.learning_notes", errors)
        if "design_considerations" in technology:
            _string_array(
                technology["design_considerations"],
                f"{prefix}.design_considerations",
                errors,
            )
        _validate_evidence(technology.get("evidence"), f"{prefix}.evidence", errors)

    flows = document.get("flows")
    if not isinstance(flows, list):
        errors.append("flows must be an array")
        flows = []
    for flow_index, flow in enumerate(flows):
        prefix = f"flows[{flow_index}]"
        if not isinstance(flow, dict):
            errors.append(f"{prefix} must be an object")
            continue
        unexpected = set(flow) - {"title", "steps"}
        if unexpected:
            errors.append(f"{prefix} has unexpected fields: " + ", ".join(sorted(unexpected)))
        _text(flow.get("title"), f"{prefix}.title", errors)
        steps = flow.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{prefix}.steps must be an array with at least one item")
            continue
        for step_index, step in enumerate(steps):
            step_prefix = f"{prefix}.steps[{step_index}]"
            if not isinstance(step, dict):
                errors.append(f"{step_prefix} must be an object")
                continue
            unexpected = set(step) - {"label", "detail", "technologies", "evidence"}
            if unexpected:
                errors.append(
                    f"{step_prefix} has unexpected fields: " + ", ".join(sorted(unexpected))
                )
            for field in ("label", "detail"):
                _text(step.get(field), f"{step_prefix}.{field}", errors)
            _string_array(step.get("technologies"), f"{step_prefix}.technologies", errors)
            if isinstance(step.get("technologies"), list):
                for name in step["technologies"]:
                    if isinstance(name, str) and name.strip() not in technology_names:
                        errors.append(
                            f"{step_prefix} references unknown technology {name!r}"
                        )
            _validate_evidence(step.get("evidence"), f"{step_prefix}.evidence", errors)

    _string_array(document.get("study_questions"), "study_questions", errors)
    return errors


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _evidence_list(entries: list[dict[str, str]], language: str) -> str:
    rows = []
    for entry in entries:
        source_label = "代码证据" if entry["source_type"] == "REPOSITORY" else "用户材料"
        if language == "en-US":
            source_label = (
                "Repository evidence"
                if entry["source_type"] == "REPOSITORY"
                else "User-provided material"
            )
        rows.append(
            '<li><span class="source-badge">'
            + _escape(source_label)
            + '</span><code>'
            + _escape(entry["citation"])
            + "</code><span>"
            + _escape(entry["supports"])
            + "</span></li>"
        )
    return "<ul class=\"evidence-list\">" + "".join(rows) + "</ul>"


def _text_list(items: list[str], class_name: str = "") -> str:
    class_attr = f' class="{_escape(class_name)}"' if class_name else ""
    return f"<ul{class_attr}>" + "".join(f"<li>{_escape(item.strip())}</li>" for item in items) + "</ul>"


def render_html(document: dict[str, Any]) -> str:
    language = document["language"]
    project_name = _escape(document["project_name"].strip())
    overview = _escape(document["project_overview"].strip())
    labels = {
        "zh-CN": {
            "title": "项目技术栈学习指南",
            "overview": "项目简介",
            "stack": "技术栈总览",
            "technology_column": "技术",
            "role_column": "项目中的职责",
            "technology_details": "逐项技术讲解",
            "role": "项目职责",
            "usage": "项目中的用法",
            "integration": "与其他组件的协作",
            "learning": "技术原理学习",
            "considerations": "实现特点与注意点",
            "evidence": "代码证据",
            "flows": "关键业务流程",
            "questions": "复习问题",
            "general_note": "以下是技术概念讲解，用于辅助学习；它不代表项目一定实现了这些概念。",
        },
        "en-US": {
            "title": "Project Technology Learning Guide",
            "overview": "Project overview",
            "stack": "Technology map",
            "technology_column": "Technology",
            "role_column": "Role in this project",
            "technology_details": "Technology details",
            "role": "Role in this project",
            "usage": "How the project uses it",
            "integration": "Integration with other components",
            "learning": "Technology concepts",
            "considerations": "Implementation notes",
            "evidence": "Code evidence",
            "flows": "Key business flows",
            "questions": "Review questions",
            "general_note": "These notes explain general concepts for study; they do not imply that the project implements each concept.",
        },
    }[language]

    rows = []
    sections = []
    for index, technology in enumerate(document["technologies"]):
        name = _escape(technology["name"].strip())
        tech_id = f"technology-{index + 1}"
        rows.append(
            f'<tr><td><a href="#{tech_id}">{name}</a></td>'
            f'<td>{_escape(technology["role"].strip())}</td></tr>'
        )
        learning_notes = _text_list(technology["learning_notes"])
        considerations = technology.get("design_considerations", [])
        consideration_markup = ""
        if considerations:
            consideration_markup = (
                f'<h4>{_escape(labels["considerations"])}</h4>'
                + _text_list(considerations)
            )
        sections.append(
            f'<section class="technology-section" id="{tech_id}">'
            f'<h3>{name}</h3>'
            f'<h4>{_escape(labels["role"])}</h4><p>{_escape(technology["role"].strip())}</p>'
            f'<h4>{_escape(labels["usage"])}</h4><p>{_escape(technology["project_usage"].strip())}</p>'
            f'<h4>{_escape(labels["integration"])}</h4><p>{_escape(technology["integration"].strip())}</p>'
            f'<h4>{_escape(labels["learning"])}</h4>'
            f'<p class="note">{_escape(labels["general_note"])}</p>{learning_notes}'
            f'{consideration_markup}'
            f'<h4>{_escape(labels["evidence"])}</h4>{_evidence_list(technology["evidence"], language)}'
            '</section>'
        )

    flow_sections = []
    for flow in document["flows"]:
        steps = []
        for step in flow["steps"]:
            used_technologies = step["technologies"]
            tech_markup = ""
            if used_technologies:
                tech_markup = '<p class="flow-tech">' + _escape(" → ".join(used_technologies)) + "</p>"
            steps.append(
                '<li class="flow-step">'
                f'<strong>{_escape(step["label"].strip())}</strong>'
                f'<p>{_escape(step["detail"].strip())}</p>'
                f'{tech_markup}{_evidence_list(step["evidence"], language)}'
                '</li>'
            )
        flow_sections.append(
            '<article class="flow">'
            f'<h3>{_escape(flow["title"].strip())}</h3>'
            f'<ol>{"".join(steps)}</ol>'
            '</article>'
        )

    flow_markup = ""
    if flow_sections:
        flow_markup = (
            f'<section class="major-section"><h2>{_escape(labels["flows"])}</h2>'
            + "".join(flow_sections)
            + "</section>"
        )
    questions_markup = ""
    if document["study_questions"]:
        questions_markup = (
            f'<section class="major-section"><h2>{_escape(labels["questions"])}</h2>'
            + _text_list(document["study_questions"], "questions")
            + "</section>"
        )

    return f'''<!doctype html>
<html lang="{_escape(language)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{project_name} - {_escape(labels["title"])}</title>
  <style>
    @page {{ size: A4 portrait; margin: 13mm 12mm 14mm; }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      color: #444;
      background: #fff;
      font-family: "Noto Sans CJK SC", "Microsoft YaHei", "PingFang SC",
        "WenQuanYi Micro Hei", Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.48;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page {{ width: 100%; }}
    .title-banner {{
      display: inline-block;
      margin: 0 0 1mm;
      padding: 2mm 5mm 2.2mm;
      color: #fff;
      background: #061f70;
      font-size: 18pt;
      font-weight: 700;
    }}
    .rule {{ height: 0.55mm; margin: 0 0 3mm; background: #061f70; }}
    h1 {{ margin: 0 0 2mm; color: #333; font-size: 16pt; }}
    h2 {{
      margin: 6mm 0 2mm;
      padding-bottom: 1mm;
      border-bottom: 0.3mm solid #9aa6c5;
      color: #102c73;
      font-size: 13pt;
    }}
    h3 {{ margin: 3mm 0 1mm; color: #273c70; font-size: 11.5pt; }}
    h4 {{ margin: 2.2mm 0 0.5mm; color: #444; font-size: 10pt; }}
    p {{ margin: 0 0 1.2mm; }}
    .overview {{ padding: 2mm 2.5mm; background: #f4f6fa; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1.5mm 0; }}
    th, td {{ border: 0.25mm solid #d3d8e2; padding: 1.5mm 2mm; text-align: left; vertical-align: top; }}
    th {{ background: #edf0f6; color: #333; }}
    ul, ol {{ margin: 0 0 1.5mm; padding-left: 6mm; }}
    li {{ margin: 0.6mm 0; }}
    a {{ color: #102c73; text-decoration: none; }}
    .technology-section {{ margin: 3mm 0 4mm; padding-top: 1mm; border-top: 0.25mm solid #d3d8e2; }}
    h2, h3, h4 {{ break-after: avoid; page-break-after: avoid; }}
    .note {{ color: #687080; font-size: 9pt; font-style: italic; }}
    .evidence-list {{ list-style: none; padding: 0 0 0 2mm; font-size: 8.5pt; }}
    .evidence-list li {{ display: flex; gap: 2mm; align-items: baseline; }}
    .source-badge {{ flex: 0 0 auto; color: #53637f; font-size: 8pt; font-weight: 700; }}
    code {{ color: #233d78; font-family: "SFMono-Regular", Consolas, monospace; font-size: 8.5pt; white-space: nowrap; }}
    .flow {{ margin: 2mm 0 3mm; break-inside: avoid; page-break-inside: avoid; }}
    .flow-step {{ margin-bottom: 2mm; }}
    .flow-tech {{ color: #596989; font-size: 9pt; }}
    .questions li {{ margin-bottom: 1mm; }}
    @media screen {{ body {{ max-width: 210mm; min-height: 297mm; margin: 0 auto; padding: 13mm 12mm 14mm; }} }}
  </style>
</head>
<body>
  <main class="page">
    <div class="title-banner">{_escape(labels["title"])}</div>
    <div class="rule"></div>
    <h1>{project_name}</h1>
    <section>
      <h2>{_escape(labels["overview"])}</h2>
      <p class="overview">{overview}</p>
      {_evidence_list(document["overview_evidence"], language)}
    </section>
    <section class="major-section">
      <h2>{_escape(labels["stack"])}</h2>
      <table><thead><tr><th>{_escape(labels["technology_column"])}</th><th>{_escape(labels["role_column"])}</th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table>
    </section>
    {flow_markup}
    <section class="major-section">
      <h2>{_escape(labels["technology_details"])}</h2>
      {"".join(sections)}
    </section>
    {questions_markup}
  </main>
</body>
</html>
'''


def find_chromium(explicit: str | None) -> str | None:
    candidate = explicit or os.environ.get("CAREER_MINER_CHROMIUM")
    if candidate:
        return shutil.which(candidate) or (
            str(Path(candidate).resolve()) if Path(candidate).is_file() else None
        )
    for name in CHROMIUM_NAMES:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def render_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    command = [
        browser,
        "--headless",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        command.insert(1, "--no-sandbox")
    result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode != 0 or not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Chromium did not create a PDF"
        raise RuntimeError(detail[-1500:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path, help="project-learning guide JSON source")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="directory for project-learning-guide.html and .pdf",
    )
    parser.add_argument("--browser", help="Chromium executable; overrides PATH discovery")
    parser.add_argument("--html-only", action="store_true", help="write HTML without invoking Chromium")
    args = parser.parse_args()

    try:
        document = json.loads(args.input_json.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"ERROR: cannot read input JSON: {error}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as error:
        print(
            f"ERROR: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}",
            file=sys.stderr,
        )
        return 2

    errors = validate_document(document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "project-learning-guide.html"
    pdf_path = output_dir / "project-learning-guide.pdf"
    html_path.write_text(render_html(document), encoding="utf-8")
    print(f"HTML: {html_path}")

    if args.html_only:
        return 0
    browser = find_chromium(args.browser)
    if not browser:
        print(
            "ERROR: Chromium was not found. Install Chromium, pass --browser, or use --html-only.",
            file=sys.stderr,
        )
        return 2
    try:
        render_pdf(browser, html_path, pdf_path)
    except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
        print(f"ERROR: PDF rendering failed: {error}", file=sys.stderr)
        print("The printable HTML file was kept.", file=sys.stderr)
        return 2
    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
