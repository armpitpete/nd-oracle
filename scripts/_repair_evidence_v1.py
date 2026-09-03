from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


# 1. Preserve the frozen one-script architecture. Evidence remains entirely no-script.
build_path = "scripts/build_site.py"
build = read(build_path)
if "# ---- Evidence Layer v1 no-script compatibility ----" not in build:
    marker = "\n# ---- command-line entrypoint ----\n"
    block = r'''
# ---- Evidence Layer v1 no-script compatibility ----
import re as _evidence_v1_re
_EVIDENCE_V1_NOJS_BASE_BUILD = build


def build(output_dir=_compat06__DEFAULT_OUTPUT_DIR):
    destination = _EVIDENCE_V1_NOJS_BASE_BUILD(output_dir)
    evidence_index = destination / 'evidence' / 'index.html'
    if not evidence_index.is_file():
        raise ValueError('Evidence Layer v1 index was not generated')
    text = evidence_index.read_text(encoding='utf-8')
    text = text.replace('<script src="/evidence-find.js" defer></script>', '')
    text = _evidence_v1_re.sub(
        r'<section aria-labelledby="evidence-search-heading">.*?</section>',
        '<section aria-labelledby="evidence-search-heading"><h2 id="evidence-search-heading">Find a source locally</h2><p>This catalogue sends no search query anywhere and loads no script. Use your browser’s built-in <strong>Find in page</strong> command (usually Ctrl+F or Command+F), or browse the source-kind groups below.</p></section>',
        text,
        count=1,
        flags=_evidence_v1_re.S,
    )
    evidence_index.write_text(text, encoding='utf-8')
    generated_script = destination / 'evidence-find.js'
    if generated_script.exists():
        generated_script.unlink()
    return destination

'''
    if marker not in build:
        raise RuntimeError("build_site command-line marker missing")
    build = build.replace(marker, "\n" + block + marker, 1)
write(build_path, build)

# Remove the public Evidence script tag at its source as well, while tolerating the
# original generator retaining an unused string constant until a later cleanup.
evidence_public_path = "scripts/evidence_public.py"
evidence_public = read(evidence_public_path)
evidence_public = evidence_public.replace('<script src="/evidence-find.js" defer></script>', '')
write(evidence_public_path, evidence_public)

# 2. Restore the accepted retrospective-audit meaning: a later review date is not
# an overdue record when a historical as-of date is intentionally used.
freshness_path = "scripts/check_content_freshness.py"
freshness = read(freshness_path)
freshness = freshness.replace(" or self.age_days < 0", "")
freshness = freshness.replace("self.age_days < 0 or ", "")
write(freshness_path, freshness)

# 3. Audit all 60 governed source records separately, applying source-kind cadence
# to legacy sources through their parent Concept's governed review date.
source_freshness = r'''#!/usr/bin/env python3
"""Audit review freshness for every governed Evidence source record."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "contracts" / "evidence-layer-v1.json"


@dataclass(frozen=True)
class EvidenceSourceFreshnessRecord:
    evidence_id: str
    evidence_model: str
    source_kind: str
    path: Path
    last_reviewed: date | None
    age_days: int | None
    max_age_days: int

    @property
    def overdue(self) -> bool:
        return self.last_reviewed is None or self.age_days is None or self.age_days > self.max_age_days


def _policy(root: Path) -> dict[str, int]:
    path = root / "contracts" / "evidence-layer-v1.json"
    raw = json.loads(path.read_text(encoding="utf-8"))["freshness"]["source_kind_max_age_days"]
    return {str(key): int(value) for key, value in raw.items()}


def _review_date(obj: dict) -> date | None:
    raw = obj.get("provenance", {}).get("last_reviewed")
    try:
        return date.fromisoformat(raw) if raw else None
    except (TypeError, ValueError):
        return None


def audit_evidence_source_freshness(root: Path = ROOT, *, as_of: date | None = None) -> list[EvidenceSourceFreshnessRecord]:
    if as_of is None:
        as_of = date.today()
    policy = _policy(root)
    records: list[EvidenceSourceFreshnessRecord] = []
    for path in sorted((root / "objects").glob("*/*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        reviewed = _review_date(obj)
        age = (as_of - reviewed).days if reviewed is not None else None
        if obj.get("type") == "concept" and obj.get("schema_version") == "0.1":
            for source in obj.get("sources", []):
                kind = str(source.get("kind", "other"))
                if kind not in policy:
                    raise ValueError(f"Unknown Evidence source_kind for freshness policy: {kind}")
                records.append(EvidenceSourceFreshnessRecord(
                    evidence_id=f"legacy:{obj['id']}:{source.get('id')}",
                    evidence_model="legacy_v0.1_embedded",
                    source_kind=kind,
                    path=path,
                    last_reviewed=reviewed,
                    age_days=age,
                    max_age_days=policy[kind],
                ))
        elif obj.get("type") == "evidence" and obj.get("schema_version") == "0.2":
            kind = str(obj.get("source_kind", "other"))
            if kind not in policy:
                raise ValueError(f"Unknown Evidence source_kind for freshness policy: {kind}")
            records.append(EvidenceSourceFreshnessRecord(
                evidence_id=str(obj.get("id", path.stem)),
                evidence_model="normalized_v0.2",
                source_kind=kind,
                path=path,
                last_reviewed=reviewed,
                age_days=age,
                max_age_days=policy[kind],
            ))
    return sorted(records, key=lambda record: record.evidence_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit all governed Evidence source review dates.")
    parser.add_argument("--as-of", help="Override today's date with YYYY-MM-DD.")
    parser.add_argument("--fail-overdue", action="store_true")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    records = audit_evidence_source_freshness(ROOT, as_of=as_of)
    overdue = [record for record in records if record.overdue]
    for record in overdue:
        reviewed = record.last_reviewed.isoformat() if record.last_reviewed else "MISSING/INVALID"
        age = str(record.age_days) if record.age_days is not None else "unknown"
        print(
            f"OVERDUE EVIDENCE SOURCE {record.evidence_id}: model={record.evidence_model}; "
            f"source_kind={record.source_kind}; last_reviewed={reviewed}; age_days={age}; "
            f"limit={record.max_age_days}; path={record.path.relative_to(ROOT)}"
        )
    print(f"Evidence source freshness audit: {len(records)} governed source records checked; {len(overdue)} overdue as of {as_of.isoformat()}.")
    return 1 if args.fail_overdue and overdue else 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
write("scripts/evidence_source_freshness.py", source_freshness)

# 4. Make the new source-level freshness audit a normal CI gate.
workflow_path = ".github/workflows/validate.yml"
workflow = read(workflow_path)
if "Audit Evidence source freshness" not in workflow:
    marker = "      - name: Audit content freshness\n"
    addition = "      - name: Audit Evidence source freshness\n        run: python scripts/evidence_source_freshness.py --fail-overdue\n\n"
    if marker not in workflow:
        raise RuntimeError("validation workflow freshness marker missing")
    workflow = workflow.replace(marker, addition + marker, 1)
write(workflow_path, workflow)

# 5. Replace provisional Evidence tests with the frozen-boundary-compatible acceptance suite.
test_layer = r'''from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_site, discovery


class EvidenceLayerV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "dist"
        build_site.build(cls.output)
        cls.evidence_dirs = sorted(
            path for path in (cls.output / "evidence").iterdir() if path.is_dir()
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def page(self, route: str) -> str:
        path = self.output / route.strip("/") / "index.html"
        self.assertTrue(path.is_file(), route)
        return path.read_text(encoding="utf-8")

    def test_sixty_source_detail_routes_plus_index_expand_contract_to_238(self) -> None:
        self.assertEqual(60, len(self.evidence_dirs))
        self.assertEqual(238, build_site.V10_ROUTE_COUNT)
        paths = build_site.sitemap_paths(build_site.load_concepts(), build_site.load_resources(), build_site.load_questions())
        self.assertEqual(238, len(paths))
        self.assertEqual(238, len(set(paths)))
        self.assertIn("/evidence/", paths)
        self.assertEqual(61, len([path for path in paths if path.startswith("/evidence/")]))

    def test_evidence_index_is_no_script_no_form_and_supports_browser_native_find(self) -> None:
        page = self.page("/evidence/")
        self.assertIn("<h1>Evidence</h1>", page)
        self.assertIn("Find in page", page)
        self.assertIn("Ctrl+F", page)
        self.assertNotIn("<script", page)
        self.assertNotIn("<form", page)
        self.assertFalse((self.output / "evidence-find.js").exists())

    def test_normalized_projection_exposes_claim_specific_evidence_fields(self) -> None:
        page = self.page("/evidence/acas-reasonable-adjustments-2025/")
        for marker in ("Finding used here:", "Context:", "Method:", "Evidence limitations"):
            self.assertIn(marker, page)
        self.assertIn("/resources/acas-reasonable-adjustments/", page)

    def test_legacy_projection_refuses_to_infer_v02_role(self) -> None:
        legacy = next(path for path in self.evidence_dirs if path.name.startswith("legacy-"))
        page = legacy.joinpath("index.html").read_text(encoding="utf-8")
        self.assertIn("legacy", page.lower())
        self.assertTrue("not" in page.lower() and "role" in page.lower())
        self.assertIn("/understand/", page)

    def test_ordinary_find_index_remains_free_of_evidence_routes(self) -> None:
        routes = {record["route"] for record in discovery.build_index()}
        self.assertFalse(any(route.startswith("/evidence/") for route in routes))

    def test_live_markers_cover_index_and_all_sixty_details(self) -> None:
        markers = build_site.evidence_route_markers()
        self.assertEqual(61, len(markers))
        self.assertEqual(61, len({path for path, _ in markers}))
        self.assertEqual("/evidence/", markers[0][0])


if __name__ == "__main__":
    unittest.main()
'''
write("tests/test_evidence_layer_v1.py", test_layer)

source_test = r'''from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import evidence_source_freshness


class EvidenceSourceFreshnessV1Tests(unittest.TestCase):
    def write_json(self, root: Path, relative: str, obj: dict) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")

    def write_policy(self, root: Path) -> None:
        path = root / "contracts" / "evidence-layer-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"freshness": {"source_kind_max_age_days": {"peer_reviewed": 730, "authoritative_guidance": 180, "community": 180, "other": 365}}}), encoding="utf-8")

    def test_mutable_guidance_and_stable_research_have_different_review_cadence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/guidance.json", {"id":"guidance","type":"evidence","schema_version":"0.2","source_kind":"authoritative_guidance","provenance":{"last_reviewed":"2026-02-01"}})
            self.write_json(root, "objects/evidence/paper.json", {"id":"paper","type":"evidence","schema_version":"0.2","source_kind":"peer_reviewed","provenance":{"last_reviewed":"2025-01-01"}})
            records = {record.evidence_id: record for record in evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))}
            self.assertTrue(records["guidance"].overdue)
            self.assertFalse(records["paper"].overdue)
            self.assertEqual(180, records["guidance"].max_age_days)
            self.assertEqual(730, records["paper"].max_age_days)

    def test_legacy_source_inherits_parent_concept_review_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/concepts/example.json", {"id":"example","type":"concept","schema_version":"0.1","provenance":{"last_reviewed":"2026-08-01"},"sources":[{"id":"community-source","kind":"community"}]})
            record = evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))[0]
            self.assertEqual("legacy:example:community-source", record.evidence_id)
            self.assertEqual("legacy_v0.1_embedded", record.evidence_model)
            self.assertFalse(record.overdue)

    def test_unknown_source_kind_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/example.json", {"id":"example","type":"evidence","schema_version":"0.2","source_kind":"mystery","provenance":{"last_reviewed":"2026-09-01"}})
            with self.assertRaisesRegex(ValueError, "Unknown Evidence source_kind"):
                evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,9,3))

    def test_retrospective_as_of_date_does_not_redefine_later_review_as_overdue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.write_policy(root)
            self.write_json(root, "objects/evidence/example.json", {"id":"example","type":"evidence","schema_version":"0.2","source_kind":"peer_reviewed","provenance":{"last_reviewed":"2026-09-02"}})
            record = evidence_source_freshness.audit_evidence_source_freshness(root, as_of=date(2026,8,29))[0]
            self.assertLess(record.age_days, 0)
            self.assertFalse(record.overdue)


if __name__ == "__main__":
    unittest.main()
'''
write("tests/test_evidence_source_freshness_v1.py", source_test)

# The provisional freshness test encoded the rejected future-date semantics; replace it
# with a narrow guard that the accepted object audit still behaves retrospectively.
compat_test = r'''from __future__ import annotations

import unittest
from datetime import date

from scripts import check_content_freshness


class EvidenceFreshnessCompatibilityV1Tests(unittest.TestCase):
    def test_existing_object_freshness_audit_retains_retrospective_semantics(self) -> None:
        records = check_content_freshness.audit_freshness(check_content_freshness.ROOT, as_of=date(2026, 8, 29))
        self.assertEqual([], [record for record in records if record.overdue])

    def test_normalized_evidence_source_kind_policy_is_present(self) -> None:
        self.assertEqual(180, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["authoritative_guidance"])
        self.assertEqual(730, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["peer_reviewed"])
        self.assertEqual(1095, check_content_freshness.EVIDENCE_SOURCE_KIND_MAX_AGE_DAYS["historical"])


if __name__ == "__main__":
    unittest.main()
'''
write("tests/test_evidence_freshness_v1.py", compat_test)

# 6. Reconcile docs away from the rejected second-script implementation.
for path in ("README.md", "docs/EVIDENCE_LAYER_STATE_v1.md", "docs/EVIDENCE_LAYER_ACCEPTANCE_v1.md", "docs/EVIDENCE_LAYER_CONTRACT_v1.md"):
    text = read(path)
    replacements = {
        "browser-local Evidence search": "static local Evidence browsing",
        "browser-local evidence search": "static local Evidence browsing",
        "local Evidence search": "static local Evidence browsing",
        "local evidence search": "static local Evidence browsing",
        "Evidence search": "Evidence browsing",
        "evidence search": "evidence browsing",
        "evidence-find.js": "no additional Evidence script",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    write(path, text)

# README validation commands should expose both evidence gates.
readme = read("README.md")
anchor = "python scripts/evidence_coverage.py --summary --fail-gaps\n"
if "python scripts/evidence_source_freshness.py --fail-overdue" not in readme:
    if anchor not in readme:
        raise RuntimeError("README evidence coverage command marker missing")
    readme = readme.replace(anchor, anchor + "python scripts/evidence_source_freshness.py --fail-overdue\n", 1)
write("README.md", readme)

print("Evidence Layer v1 frozen-boundary repair prepared")
