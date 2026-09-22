from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "site" / "resource-media" / "a-kind-of-spark.jpg"
EXPECTED_SHA256 = "483dc7fd0daa8bc473b449c298737e943a717a3e544f2bd48650d272f021d7d7"
EXPECTED_BYTES = 1478012


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected exactly one marker, found {text.count(old)}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def verify_asset() -> None:
    raw = ASSET.read_bytes()
    if len(raw) != EXPECTED_BYTES:
        raise SystemExit(f"unexpected cover size: {len(raw)}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"unexpected cover sha256: {digest}")
    if raw[:3] != bytes.fromhex("ffd8ff"):
        raise SystemExit("cover is not a JPEG")


def update_registry() -> None:
    path = ROOT / "site" / "resource-visuals.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["reviewed_on"] = "2026-09-22"
    entry = registry["entries"]["a-kind-of-spark"]
    entry.update({
        "status": "cleared",
        "source_url": "https://www.panmacmillan.com/authors/elle-mcnicoll/a-kind-of-spark/9781037410642",
        "rights_holder": "Pan Macmillan",
        "rights_basis": "Written permission from PanMac Permissions on 2026-09-22 for ND Oracle to reproduce the supplied A Kind of Spark cover, subject to no alterations to the image and no defamatory or negative references to the book.",
        "local_path": "site/resource-media/a-kind-of-spark.jpg",
        "alt": "Cover of A Kind of Spark by Elle McNicoll.",
        "attribution": None,
        "checked_on": "2026-09-22",
        "rights_note": "PanMac Permissions supplied the exact cover file and granted the requested ND Oracle web use. The supplied JPEG must remain byte-for-byte unaltered; display sizing is CSS/browser-only. The permission is conditional on no defamatory or negative references to the book, so any material future editorial change to this Resource requires a fresh rights review before the visual remains publishable.",
        "attribution_required": False,
        "rights_research_state": "cleared-written-permission-exact-attached-cover-unaltered",
        "rights_review_url": "https://www.panmacmillan.com/terms-and-conditions",
        "permission_route": "PanMac Permissions <panmac.permissions@macmillan.com>",
        "rights_candidate_basis": "Written permission received from PanMac Permissions on 2026-09-22.",
        "asset_strategy": "Use the exact publisher-supplied JPEG bytes unchanged; resize only at presentation time with CSS/browser layout.",
        "permission_evidence": "docs/RESOURCE_VISUAL_RIGHTS_A_KIND_OF_SPARK_v1.md",
        "recheck_trigger": "Any material editorial change to the A Kind of Spark Resource commentary requires manual re-review of the image permission condition."
    })
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_rights_evidence() -> None:
    path = ROOT / "docs" / "RESOURCE_VISUAL_RIGHTS_A_KIND_OF_SPARK_v1.md"
    path.write_text("""# A Kind of Spark Resource Visual Rights Evidence v1

Date: 2026-09-22
Resource ID: `a-kind-of-spark`
Status: CLEARED / CANDIDATE BRANCH ONLY

## Permission

- Rights contact: PanMac Permissions (`panmac.permissions@macmillan.com`).
- Permission received: 2026-09-22.
- ND Oracle requested public web display on ndoracle.org, worldwide access, local hosting, a modest recognition/navigation image, and no endorsement implication.
- PanMac Permissions granted the requested use and supplied the appropriate cover file.
- Conditions: the image must not be altered; the book must not be accompanied by defamatory or negative references.
- Attribution requirement stated in the permission response: none.
- Re-review trigger: any material future editorial change to the Resource commentary requires a fresh manual rights check before the image remains publishable.

## Exact supplied asset

- Attachment filename: `9781037410642.jpg`
- Published local path: `site/resource-media/a-kind-of-spark.jpg`
- Format: JPEG
- Dimensions: 1561 × 2398
- Size: 1,478,012 bytes
- SHA-256: `483dc7fd0daa8bc473b449c298737e943a717a3e544f2bd48650d272f021d7d7`
- Transformation: none. The publisher-supplied bytes are retained unchanged.
- Presentation sizing: CSS/browser layout only; no derivative image is generated.

## Editorial boundary

The image permission is evidence about image reuse only. It does not change the governed Resource object, Claims, Evidence, ranking, endorsement or editorial authority. If the permission condition and future editorial treatment become incompatible, the visual must fail closed rather than constrain ND Oracle's editorial record.
""", encoding="utf-8")


def update_full_corpus_register() -> None:
    path = ROOT / "docs" / "RESOURCE_VISUAL_FULL_CORPUS_REGISTER_v1.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Date: 2026-09-18", "Date: 2026-09-22", 1)
    text = text.replace("- `permission-required`: **26**", "- `permission-required`: **25**", 1)
    text = text.replace("- `cleared`: **1**", "- `cleared`: **5**", 1)
    old = "| `a-kind-of-spark` — A Kind of Spark — Elle McNicoll | book | yes | `permission-required` | permission-route-confirmed |"
    new = "| `a-kind-of-spark` — A Kind of Spark — Elle McNicoll | book | yes | `cleared` | cleared-written-permission-exact-attached-cover-unaltered |"
    if old not in text:
        raise SystemExit("full corpus A Kind of Spark row marker missing")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


def update_permission_queue() -> None:
    path = ROOT / "docs" / "RESOURCE_VISUAL_PERMISSION_QUEUE_v1.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Date: 2026-09-18", "Date: 2026-09-22", 1)
    text = text.replace("- Cleared for publication: **4**", "- Cleared for publication: **5**", 1)
    text = text.replace("- Permission required: **26**", "- Permission required: **25**", 1)
    row = "| `a-kind-of-spark` — A Kind of Spark — Elle McNicoll | book | `permission-required` | Pan Macmillan | permission-route-confirmed | childrenspermissions@macmillan.com |\n"
    if row not in text:
        raise SystemExit("permission queue A Kind of Spark row missing")
    text = text.replace(row, "", 1)
    text = text.replace("3. **Macmillan:** `a-kind-of-spark` and `front-of-the-class`.", "3. **Macmillan:** `front-of-the-class`.", 1)
    marker = "- Rights/asset binding unresolved: **7**\n"
    note = marker + "- Resolved 2026-09-22: `a-kind-of-spark` moved to `cleared` on written Pan Macmillan permission with the exact supplied cover retained unaltered.\n"
    if marker not in text:
        raise SystemExit("permission queue summary marker missing")
    text = text.replace(marker, note, 1)
    path.write_text(text, encoding="utf-8")


def update_tests() -> None:
    path = ROOT / "tests" / "test_resource_visual_full_corpus_v1.py"
    text = path.read_text(encoding="utf-8")
    if "import hashlib\n" not in text:
        text = text.replace("from __future__ import annotations\n\n", "from __future__ import annotations\n\nimport hashlib\n", 1)
    text = text.replace('self.assertEqual(4, sum(entry["status"] == "cleared" for entry in entries))',
                        'self.assertEqual(5, sum(entry["status"] == "cleared" for entry in entries))', 1)
    text = text.replace('self.assertEqual(26, sum(entry["status"] == "permission-required" for entry in entries))',
                        'self.assertEqual(25, sum(entry["status"] == "permission-required" for entry in entries))', 1)
    marker = "    def test_corrupt_cleared_asset_fails_closed(self) -> None:\n"
    addition = '''    def test_a_kind_of_spark_permission_and_exact_asset_are_frozen(self) -> None:
        registry = resource_visuals.load_registry()
        entry = registry["entries"]["a-kind-of-spark"]
        self.assertEqual("cleared", entry["status"])
        self.assertEqual("cleared-written-permission-exact-attached-cover-unaltered", entry["rights_research_state"])
        self.assertIn("must remain byte-for-byte unaltered", entry["rights_note"])
        self.assertIn("future editorial change", entry["rights_note"])
        asset = ROOT / entry["local_path"]
        raw = asset.read_bytes()
        self.assertEqual(1478012, len(raw))
        self.assertEqual(
            "483dc7fd0daa8bc473b449c298737e943a717a3e544f2bd48650d272f021d7d7",
            hashlib.sha256(raw).hexdigest(),
        )

'''
    if addition not in text:
        if marker not in text:
            raise SystemExit("test insertion marker missing")
        text = text.replace(marker, addition + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_visual_evidence_workflow() -> None:
    path = ROOT / ".github" / "workflows" / "ux-visual-evidence.yml"
    text = path.read_text(encoding="utf-8")
    grep_marker = '          grep -q \'src="/resource-media/townscaper.jpg"\' candidate/dist/resources/townscaper/index.html\n'
    grep_new = '          grep -q \'src="/resource-media/a-kind-of-spark.jpg"\' candidate/dist/resources/a-kind-of-spark/index.html\n' + grep_marker
    if 'src="/resource-media/a-kind-of-spark.jpg"' not in text:
        if grep_marker not in text:
            raise SystemExit("visual workflow grep marker missing")
        text = text.replace(grep_marker, grep_new, 1)

    route_marker = '            "resource-goblin-tools|/resources/goblin-tools/"\n'
    route_new = route_marker + '            "resource-a-kind-of-spark|/resources/a-kind-of-spark/"\n'
    if '"resource-a-kind-of-spark|/resources/a-kind-of-spark/"' not in text:
        if route_marker not in text:
            raise SystemExit("visual workflow route marker missing")
        text = text.replace(route_marker, route_new, 1)

    manifest_marker = '            echo "resource_townscaper_capture=1440x1100,390x844"\n'
    manifest_new = '            echo "resource_a_kind_of_spark_capture=1440x1100,390x844"\n' + manifest_marker
    if 'resource_a_kind_of_spark_capture=' not in text:
        if manifest_marker not in text:
            raise SystemExit("visual workflow manifest marker missing")
        text = text.replace(manifest_marker, manifest_new, 1)

    text = text.replace('test "$(find ux-evidence/baseline -name \'*.png\' | wc -l)" -eq 54',
                        'test "$(find ux-evidence/baseline -name \'*.png\' | wc -l)" -eq 56', 1)
    text = text.replace('test "$(find ux-evidence/candidate -name \'*.png\' | wc -l)" -eq 54',
                        'test "$(find ux-evidence/candidate -name \'*.png\' | wc -l)" -eq 56', 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    verify_asset()
    update_registry()
    write_rights_evidence()
    update_full_corpus_register()
    update_permission_queue()
    update_tests()
    update_visual_evidence_workflow()


if __name__ == "__main__":
    main()
