from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH_QUESTION_IDS = {
    "adult-autism-assessment-england",
    "adult-adhd-assessment-england",
    "adult-autism-assessment-scotland",
    "adult-adhd-assessment-scotland",
    "adult-autism-assessment-wales",
    "adult-adhd-assessment-wales",
    "adult-autism-assessment-northern-ireland",
    "adult-adhd-assessment-northern-ireland",
    "child-autism-assessment-england",
    "child-adhd-assessment-england",
    "child-autism-assessment-scotland",
    "child-adhd-assessment-scotland",
    "child-autism-assessment-wales",
    "child-adhd-assessment-wales",
    "child-autism-assessment-northern-ireland",
    "child-adhd-assessment-northern-ireland",
    "private-autism-adhd-assessment-uk",
    "waiting-for-autism-adhd-assessment-uk",
    "assessment-refused-or-disagree-uk",
    "after-autism-adhd-assessment-uk",
    "assessment-communication-sensory-adjustments-uk",
    "co-occurring-autism-adhd-assessment-uk",
    "other-neurodevelopmental-assessments-uk",
}


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def resolve_pointer(document: object, pointer: str) -> object:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(pointer)
    current = document
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[part]
        elif isinstance(current, list):
            current = current[int(part)]
        else:
            raise KeyError(pointer)
    return current


# The accepted public Question renderer supports related Concepts and Resources,
# but not Question-to-Question references. Keep the cross-cutting narrative in
# current_understanding and expose sibling Questions through the Assessment hub.
for question_id in sorted(BRANCH_QUESTION_IDS):
    path = ROOT / "objects" / "questions" / f"{question_id}.json"
    if not path.is_file():
        raise SystemExit(f"missing Assessment question: {question_id}")
    document = json.loads(path.read_text(encoding="utf-8"))
    before = list(document["related_objects"])
    document["related_objects"] = [item for item in before if item.get("type") != "question"]
    if not document["related_objects"]:
        raise SystemExit(f"filtering related Questions would leave {question_id} unlinked")
    if document["related_objects"] != before:
        path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

# Preserve the exact accepted-production wording that is bound by release-state
# regression tests while still describing the repository candidate separately.
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
old = "Production is still the accepted v1.2 release"
new = "Production is the accepted v1.2 release"
if old not in text:
    raise SystemExit("README production-state repair anchor missing")
readme.write_text(text.replace(old, new, 1), encoding="utf-8")

# These two tests deliberately assert the *current* corpus, not their frozen
# historical fixture subsets. Advance only those current-count assertions.
old_counts = '{"concepts": 20, "resources": 76, "questions": 55, "evidence": 3}'
new_counts = '{"concepts": 20, "resources": 91, "questions": 76, "evidence": 3}'
for relative in ("tests/test_v12_healthcare_parity.py", "tests/test_v12_need_coverage.py"):
    path = ROOT / relative
    body = path.read_text(encoding="utf-8")
    if old_counts not in body:
        raise SystemExit(f"current-count repair anchor missing: {relative}")
    path.write_text(body.replace(old_counts, new_counts, 1), encoding="utf-8")

# Bind every additive scoped route to the exact committed governed field and
# declared scope using the frozen v1.1 canonical hashing contract.
extension_path = ROOT / "discovery" / "assessment-diagnosis-uk-v1.json"
extension = json.loads(extension_path.read_text(encoding="utf-8"))
routes = extension["scope_provenance"]["routes"]
if len(routes) != 29:
    raise SystemExit(f"expected 29 Assessment scoped routes, found {len(routes)}")
for route, entry in routes.items():
    parts = route.strip("/").split("/")
    if len(parts) != 2 or parts[0] not in {"questions", "resources"}:
        raise SystemExit(f"unsupported scoped route: {route}")
    source = ROOT / "objects" / parts[0] / f"{parts[1]}.json"
    document = json.loads(source.read_text(encoding="utf-8"))
    value = resolve_pointer(document, entry["basis_path"])
    basis_sha = hashlib.sha256(canonical(value)).hexdigest()
    binding_sha = hashlib.sha256(canonical({"basis_sha256": basis_sha, "scope": entry["scope"]})).hexdigest()
    entry["basis_sha256"] = basis_sha
    entry["binding_sha256"] = binding_sha
extension_path.write_text(json.dumps(extension, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

# The mutation machinery is branch-only evidence and must not survive into the
# candidate diff.
(ROOT / "scripts" / "_repair_assessment_candidate_once.py").unlink(missing_ok=True)
(ROOT / ".github" / "workflows" / "assessment-candidate-repair-one-shot.yml").unlink(missing_ok=True)
