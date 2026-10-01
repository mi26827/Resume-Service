import re
import unittest
from pathlib import Path

from scripts.validate_output import validate


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = REPOSITORY_ROOT / "examples" / "tiny-task-api"
SAMPLE_OUTPUT = EXAMPLE_ROOT / "sample-output"
CITATION = re.compile(
    r"`(?P<path>(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.py):"
    r"(?P<start>\d+)(?:-(?P<end>\d+))?`"
)


class ExampleReportTest(unittest.TestCase):
    def test_sample_discovery_report_passes_structural_validation(self):
        self.assertEqual(validate(SAMPLE_OUTPUT), [])

    def test_every_sample_code_citation_points_to_existing_lines(self):
        report_paths = sorted(SAMPLE_OUTPUT.glob("*.md"))
        self.assertEqual(len(report_paths), 4)
        citations_found = 0

        for report_path in report_paths:
            report = report_path.read_text(encoding="utf-8")
            for match in CITATION.finditer(report):
                citations_found += 1
                source_path = EXAMPLE_ROOT / match.group("path")
                self.assertTrue(source_path.is_file(), f"missing cited file: {source_path}")
                line_count = len(source_path.read_text(encoding="utf-8").splitlines())
                first = int(match.group("start"))
                last = int(match.group("end") or first)
                self.assertLessEqual(first, last, f"reversed range in {report_path.name}")
                self.assertGreaterEqual(first, 1, f"invalid line in {report_path.name}")
                self.assertLessEqual(last, line_count, f"line past EOF in {source_path.name}")

        self.assertGreater(citations_found, 0)


if __name__ == "__main__":
    unittest.main()
