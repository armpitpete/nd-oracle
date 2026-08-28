from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_repository

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "v0.2"
EVIDENCE = FIXTURES / "evidence" / "fixture-evidence.json"


class EvidenceDatePrecisionImplementationTests(unittest.TestCase):
    def _validate_evidence_mutation(self, mutate) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            test_root = Path(directory)
            shutil.copytree(ROOT / "schema", test_root / "schema")
            shutil.copytree(ROOT / "objects", test_root / "objects")
            fixture_root = test_root / "tests" / "fixtures" / "v0.2"
            shutil.copytree(FIXTURES, fixture_root)
            path = fixture_root / "evidence" / "fixture-evidence.json"
            obj = json.loads(path.read_text(encoding="utf-8"))
            mutate(obj)
            path.write_text(json.dumps(obj), encoding="utf-8")
            _, errors = validate_repository(test_root, fixture_root)
            return errors

    def test_exact_fixture_keeps_value_and_declares_day_precision(self) -> None:
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual("2026-08-11", evidence["date"])
        self.assertEqual("day", evidence["date_precision"])
        count, errors = validate_repository(ROOT, FIXTURES)
        authoritative_count = len(list((ROOT / "objects").rglob("*.json")))
        self.assertEqual(authoritative_count, count)
        self.assertEqual([], errors)

    def test_year_month_and_day_precision_validate(self) -> None:
        cases = (
            ("2016", "year"),
            ("2016-07", "month"),
            ("2016-07-03", "day"),
        )
        for date, precision in cases:
            with self.subTest(date=date, precision=precision):
                errors = self._validate_evidence_mutation(
                    lambda obj, date=date, precision=precision: (
                        obj.__setitem__("date", date),
                        obj.__setitem__("date_precision", precision),
                    )
                )
                self.assertEqual([], errors)

    def test_precision_value_mismatches_fail_closed(self) -> None:
        cases = (
            ("2016-07-03", "year"),
            ("2016", "day"),
            ("2016-07", "year"),
            ("2016-07-03", "month"),
        )
        for date, precision in cases:
            with self.subTest(date=date, precision=precision):
                errors = self._validate_evidence_mutation(
                    lambda obj, date=date, precision=precision: (
                        obj.__setitem__("date", date),
                        obj.__setitem__("date_precision", precision),
                    )
                )
                self.assertTrue(errors)

    def test_invalid_month_and_day_fail(self) -> None:
        cases = (
            ("2016-13", "month"),
            ("2016-00", "month"),
            ("2016-02-30", "day"),
        )
        for date, precision in cases:
            with self.subTest(date=date, precision=precision):
                errors = self._validate_evidence_mutation(
                    lambda obj, date=date, precision=precision: (
                        obj.__setitem__("date", date),
                        obj.__setitem__("date_precision", precision),
                    )
                )
                self.assertTrue(errors)

    def test_date_precision_is_required_and_bounded(self) -> None:
        missing = self._validate_evidence_mutation(lambda obj: obj.pop("date_precision"))
        self.assertTrue(missing)
        invalid = self._validate_evidence_mutation(
            lambda obj: obj.__setitem__("date_precision", "approximate")
        )
        self.assertTrue(invalid)

    def test_accessed_remains_an_exact_full_date(self) -> None:
        errors = self._validate_evidence_mutation(
            lambda obj: obj.__setitem__("accessed", "2026-08")
        )
        self.assertTrue(errors)

    def test_singer_year_only_shape_is_valid_without_day_candidate(self) -> None:
        errors = self._validate_evidence_mutation(
            lambda obj: (
                obj.__setitem__("date", "2016"),
                obj.__setitem__("date_precision", "year"),
            )
        )
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
