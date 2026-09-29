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
            if name == "08-agent-opportunity.md":
                body += "- Outcome: `NO_SUITABLE_OPPORTUNITY`\n"
            (directory / name).write_text(body, encoding="utf-8")
        return directory

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_modes(self):
        for mode in MODE_REPORTS:
            with self.subTest(mode=mode):
                self.temp_dir.cleanup()
                self.temp_dir = tempfile.TemporaryDirectory()
                self.assertEqual(validate(self.make_run(mode)), [])

    def test_rejects_stale_report(self):
        root = self.make_run("ATTRIBUTION")
        (root / "08-agent-opportunity.md").write_text(HEADER.format(mode="ATTRIBUTION"), encoding="utf-8")
        self.assertTrue(any("unexpected" in error for error in validate(root)))

    def test_rejects_inconsistent_revision(self):
        root = self.make_run("ATTRIBUTION")
        report = root / "04-contribution-evidence.md"
        report.write_text(report.read_text().replace("abc123", "def456"), encoding="utf-8")
        self.assertTrue(any("one mode and revision" in error for error in validate(root)))


if __name__ == "__main__":
    unittest.main()
