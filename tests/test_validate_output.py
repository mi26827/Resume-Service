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
    def make_run(self, mode: str) -> Path:
        directory = Path(self.temp_dir.name)
        (directory / "SUMMARY.md").write_text(HEADER.format(mode=mode), encoding="utf-8")
        for name in MODE_REPORTS[mode]:
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
        self.assertTrue(any("one mode and revision" in error for error in validate(root)))

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
