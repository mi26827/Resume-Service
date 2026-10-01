import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_output import MODE_REPORTS, validate


HEADER = """# Report

> Contract: `career-miner/0.2`
> Mode: `{mode}`
> Revision: `abc123`
> Status: `COMPLETE`

"""


class ValidateOutputTest(unittest.TestCase):
    def make_run(self, mode: str, report_names=None) -> Path:
        directory = Path(self.temp_dir.name)
        (directory / "SUMMARY.md").write_text(HEADER.format(mode=mode), encoding="utf-8")
        names = MODE_REPORTS[mode] if report_names is None else set(report_names)
        for name in names:
            body = HEADER.format(mode=mode)
            if name in {"04-contribution-evidence.md", "06-resume-bullets.md"}:
                body += "Implementation Evidence | Attribution Evidence\n"
            if name == "06-resume-bullets.md":
                body += """
## Engineering Findings
## Finding Clusters
## Project Introduction
## Technology Stack
## Architecture Design Highlights
## Final Project Experience
"""
            if name == "08-agent-opportunity.md":
                body += "- Outcome: `NO_SUITABLE_OPPORTUNITY`\n"
            (directory / name).write_text(body, encoding="utf-8")
        return directory

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_discovery_contribution_ai_agent_resume_and_full_are_valid(self):
        for mode in ("DISCOVERY", "CONTRIBUTION", "AI_AGENT", "RESUME", "FULL"):
            with self.subTest(mode=mode):
                self.temp_dir.cleanup()
                self.temp_dir = tempfile.TemporaryDirectory()
                self.assertEqual(validate(self.make_run(mode)), [])

    def test_discovery_rejects_resume_report_as_stale(self):
        root = self.make_run("DISCOVERY")
        (root / "06-resume-bullets.md").write_text(
            HEADER.format(mode="DISCOVERY") + "Implementation Evidence | Attribution Evidence\n",
            encoding="utf-8",
        )
        self.assertTrue(any("unexpected" in error for error in validate(root)))

    def test_standard_mode_rejects_unrecognized_numbered_report(self):
        root = self.make_run("DISCOVERY")
        (root / "10-old-report.md").write_text(HEADER.format(mode="DISCOVERY"), encoding="utf-8")
        self.assertTrue(any("unrecognized numbered reports" in error for error in validate(root)))

    def test_contribution_requires_backend_engineering_report(self):
        root = self.make_run("CONTRIBUTION")
        (root / "05-backend-engineering-analysis.md").unlink()
        self.assertTrue(any("missing reports" in error for error in validate(root)))

    def test_resume_does_not_require_contribution_report(self):
        root = self.make_run("RESUME")
        self.assertFalse((root / "04-contribution-evidence.md").exists())
        self.assertEqual(validate(root), [])

    def test_rejects_inconsistent_revision(self):
        root = self.make_run("CONTRIBUTION")
        report = root / "04-contribution-evidence.md"
        report.write_text(report.read_text().replace("abc123", "def456"), encoding="utf-8")
        self.assertTrue(
            any("one contract, mode, revision, and status" in error for error in validate(root))
        )

    def test_rejects_inconsistent_mode(self):
        root = self.make_run("DISCOVERY")
        report = root / "01-project-overview.md"
        report.write_text(report.read_text().replace("Mode: `DISCOVERY`", "Mode: `FULL`"), encoding="utf-8")
        self.assertTrue(
            any("one contract, mode, revision, and status" in error for error in validate(root))
        )

    def test_rejects_inconsistent_status(self):
        root = self.make_run("DISCOVERY")
        report = root / "01-project-overview.md"
        report.write_text(report.read_text().replace("Status: `COMPLETE`", "Status: `PARTIAL`"), encoding="utf-8")
        self.assertTrue(
            any("one contract, mode, revision, and status" in error for error in validate(root))
        )

    def test_rejects_unsupported_contract_header(self):
        root = self.make_run("DISCOVERY")
        summary = root / "SUMMARY.md"
        summary.write_text(summary.read_text().replace("career-miner/0.2", "career-miner/0.3"), encoding="utf-8")
        self.assertTrue(any("SUMMARY.md: missing or invalid contract header" in error for error in validate(root)))

    def test_custom_requires_an_explicit_report_list(self):
        root = self.make_run("CUSTOM", {"01-project-overview.md"})
        errors = validate(root)
        self.assertTrue(any("CUSTOM mode requires an explicit report list" in error for error in errors))

    def test_custom_rejects_an_empty_report_list(self):
        root = self.make_run("CUSTOM", set())
        errors = validate(root, custom_reports=[])
        self.assertTrue(any("CUSTOM mode requires an explicit report list" in error for error in errors))

    def test_custom_accepts_exact_selected_report_set(self):
        selected = {"01-project-overview.md", "03-architecture-analysis.md"}
        root = self.make_run("CUSTOM", selected)
        self.assertEqual(validate(root, custom_reports=sorted(selected)), [])

    def test_custom_rejects_missing_and_unrequested_reports(self):
        selected = {"01-project-overview.md", "03-architecture-analysis.md"}
        root = self.make_run("CUSTOM", selected)
        (root / "03-architecture-analysis.md").unlink()
        (root / "02-tech-stack.md").write_text(HEADER.format(mode="CUSTOM"), encoding="utf-8")
        errors = validate(root, custom_reports=sorted(selected))
        self.assertTrue(any("CUSTOM: missing reports" in error for error in errors))
        self.assertTrue(any("CUSTOM: stale or unexpected reports" in error for error in errors))

    def test_custom_rejects_duplicate_selected_reports(self):
        root = self.make_run("CUSTOM", {"01-project-overview.md"})
        errors = validate(root, custom_reports=["01-project-overview.md", "01-project-overview.md"])
        self.assertTrue(any("custom report list contains duplicates" in error for error in errors))

    def test_custom_cli_accepts_the_explicit_report_list(self):
        selected = ["01-project-overview.md", "03-architecture-analysis.md"]
        root = self.make_run("CUSTOM", selected)
        script = Path(__file__).resolve().parents[1] / "scripts" / "validate_output.py"
        result = subprocess.run(
            [sys.executable, str(script), str(root), "--custom-reports", *selected],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_custom_cli_explains_when_report_list_is_missing(self):
        root = self.make_run("CUSTOM", {"01-project-overview.md"})
        script = Path(__file__).resolve().parents[1] / "scripts" / "validate_output.py"
        result = subprocess.run(
            [sys.executable, str(script), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("CUSTOM mode requires an explicit report list", result.stderr)

    def test_resume_requires_evidence_funnel_sections(self):
        root = self.make_run("RESUME")
        report = root / "06-resume-bullets.md"
        report.write_text(
            report.read_text().replace("## Finding Clusters\n", ""), encoding="utf-8"
        )
        self.assertTrue(
            any("missing evidence-funnel sections" in error for error in validate(root))
        )


if __name__ == "__main__":
    unittest.main()
