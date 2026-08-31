from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "objects"
POLICY_PATH = ROOT / "discovery" / "routing-policy-v1.1.json"
POLICY: dict[str, Any] = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
STOP_WORDS = set(POLICY["normalization"]["stop_words"])
GENERIC_WORDS = set(POLICY["normalization"]["generic_words"])
INTENT_PHRASES = {route: tuple(values) for route, values in POLICY["intent_phrases"].items()}
_SCOPE_BY_ROUTE = POLICY["scope_provenance"]["routes"]
_POLICY_VALIDATED = False

# Compatibility export retained for v1.0 callers/tests. v1.1 boundary authority
# is clinical_boundary(), not substring membership in this tuple.
REFUSAL_PATTERNS = (
    "diagnose me", "am i autistic", "do i have autism", "do i have adhd",
    "what medication dose", "what dose should i take", "stop my medication",
    "which medication should i take", "tell me if i am autistic", "tell me if i have adhd",
)


@dataclass(frozen=True)
class SearchResult:
    route: str
    kind: str
    object_id: str
    title: str
    excerpt: str
    score: int


def _normalise(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", (value or "").casefold()))


def _tokens(value: str) -> list[str]:
    minimum = int(POLICY["normalization"]["minimum_token_length"])
    return [token for token in _normalise(value).split() if token not in STOP_WORDS and len(token) >= minimum]


def _meaningful_tokens(value: str) -> list[str]:
    return [token for token in _tokens(value) if token not in GENERIC_WORDS]


def _load_dir(name: str) -> list[dict]:
    directory = OBJECTS / name
    if not directory.is_dir():
        return []
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]


def build_index() -> list[dict]:
    records: list[dict] = []
    for item in _load_dir("questions"):
        records.append({
            "route": f"/questions/{item['id']}/",
            "kind": "Question",
            "id": item["id"],
            "title": item["question"],
            "aliases": [],
            "body": " ".join([
                item.get("why_it_matters", ""),
                item.get("current_understanding", ""),
                *item.get("evidence_needed", []),
                *item.get("dissent", []),
            ]),
        })
    for item in _load_dir("concepts"):
        aliases = list(item.get("aliases", []))
        records.append({
            "route": f"/understand/{item['id']}/",
            "kind": "Topic",
            "id": item["id"],
            "title": item["name"],
            "aliases": aliases,
            "body": " ".join([
                item.get("summary", ""),
                " ".join(aliases),
                " ".join(claim.get("text", "") for claim in item.get("claims", [])),
            ]),
        })
    for item in _load_dir("resources"):
        records.append({
            "route": f"/resources/{item['id']}/",
            "kind": "Resource",
            "id": item["id"],
            "title": item["name"],
            "aliases": [],
            "body": " ".join([
                item.get("description", ""),
                item.get("intended_use", ""),
                item.get("audience_or_context", ""),
                *item.get("limitations", []),
                *item.get("cost_or_access_notes", []),
            ]),
        })
    return sorted(records, key=lambda record: (record["kind"], _normalise(record["title"]), record["route"]))


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _resolve_json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError(f"Invalid JSON pointer: {pointer!r}")
    current = value
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise KeyError(pointer)
    return current


def validate_policy(*, policy: dict[str, Any] | None = None, index: list[dict] | None = None) -> None:
    candidate = POLICY if policy is None else policy
    if candidate.get("version") != "1.1":
        raise ValueError("Routing policy must be v1.1")

    expected_scopes = {
        "England": {"England"},
        "Scotland": {"Scotland"},
        "Wales": {"Wales"},
        "Northern Ireland": {"Northern Ireland"},
        "Great Britain": {"England", "Scotland", "Wales"},
        "England and Wales": {"England", "Wales"},
        "United Kingdom": {"England", "Scotland", "Wales", "Northern Ireland"},
    }
    scopes = candidate["jurisdiction"]["scope_sets"]
    if {name: set(values) for name, values in scopes.items()} != expected_scopes:
        raise ValueError("Jurisdiction scope sets do not match frozen v1.1")
    if candidate["jurisdiction"]["canonical_order"] != ["England", "Scotland", "Wales", "Northern Ireland"]:
        raise ValueError("Jurisdiction canonical order is incomplete or unstable")

    provenance = candidate["scope_provenance"]
    if provenance.get("basis") != "exact governed field value; any basis-value drift invalidates routing scope":
        raise ValueError("Unexpected scope provenance basis")
    if provenance.get("source_path_rule") != "objects/{route_kind}/{route_id}.json":
        raise ValueError("Unexpected scope provenance path rule")
    fingerprint = provenance.get("basis_fingerprint", {})
    if fingerprint != {"algorithm": "sha256", "serialization": "canonical-json-utf8"}:
        raise ValueError("Unexpected scope provenance fingerprint contract")

    entries = provenance.get("routes")
    if not isinstance(entries, dict) or len(entries) != 29:
        raise ValueError(f"Expected 29 frozen scoped routes, found {len(entries) if isinstance(entries, dict) else 'invalid'}")
    indexed = {record["route"] for record in (build_index() if index is None else index)}
    for route, encoded in entries.items():
        if not isinstance(encoded, dict) or set(encoded) != {"scope", "basis_path", "basis_sha256"}:
            raise ValueError(f"Malformed scope entry: {route}")
        scope = encoded["scope"]
        basis_path = encoded["basis_path"]
        expected_sha = encoded["basis_sha256"]
        if route not in indexed or scope not in scopes:
            raise ValueError(f"Invalid scoped route: {route}")
        if not isinstance(expected_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            raise ValueError(f"Invalid scope basis fingerprint: {route}")

        parts = route.strip("/").split("/")
        if len(parts) != 2 or parts[0] not in {"questions", "resources"}:
            raise ValueError(f"Unresolvable scope source: {route}")
        source = ROOT / "objects" / parts[0] / f"{parts[1]}.json"
        if not source.is_file():
            raise ValueError(f"Missing scope provenance source: {route}")
        document = json.loads(source.read_text(encoding="utf-8"))
        if document.get("id") != parts[1]:
            raise ValueError(f"Scope provenance identity mismatch: {route}")
        try:
            basis_value = _resolve_json_pointer(document, basis_path)
        except (KeyError, ValueError, IndexError, TypeError) as exc:
            raise ValueError(f"Scope provenance basis missing: {route} {basis_path}") from exc
        if not isinstance(basis_value, str) or not basis_value.strip():
            raise ValueError(f"Scope provenance basis must be a non-empty governed string: {route}")
        actual_sha = hashlib.sha256(_canonical_json_bytes(basis_value)).hexdigest()
        if actual_sha != expected_sha:
            raise ValueError(f"Scope provenance fingerprint mismatch: {route}")

    if candidate["orientation"].get("enabled") is not False:
        raise ValueError("Orientation forbidden until ablation proves it necessary")


def _ensure_policy(index: list[dict]) -> None:
    global _POLICY_VALIDATED
    if not _POLICY_VALIDATED:
        validate_policy(index=index)
        _POLICY_VALIDATED = True


def _has(normalized: str, phrase: str) -> bool:
    needle = _normalise(phrase)
    return bool(needle) and f" {needle} " in f" {normalized} "


def _has_any(normalized: str, phrases: list[str]) -> bool:
    return any(_has(normalized, phrase) for phrase in phrases)


def _clinical_clauses(query: str) -> list[str]:
    # Quoted material is mention, not an instruction. A real prohibited request
    # elsewhere in the query still survives and wins the hard boundary.
    stripped = re.sub(r'"[^"]*"|“[^”]*”', " ", query or "")
    return [
        clause for clause in re.split(r"[.!?;]+|\bbut\b", stripped, flags=re.I)
        if _normalise(clause)
    ]


def _has_person_target(normalized: str, cfg: dict[str, Any]) -> bool:
    words = set(normalized.split())
    return bool(words & set(cfg["target_terms"]))


def _has_deictic_target(normalized: str, cfg: dict[str, Any]) -> bool:
    words = set(normalized.split())
    return bool(words & set(cfg["deictic_terms"]))


def _has_condition(normalized: str, cfg: dict[str, Any]) -> bool:
    words = set(normalized.split())
    return bool(words & set(cfg["condition_terms"]))


def _has_evidence_subject(normalized: str, cfg: dict[str, Any]) -> bool:
    return _has_any(normalized, cfg["evidence_terms"])


def _direct_person_condition_question(normalized: str) -> bool:
    # Person-specific "have/be" constructions, not condition->meaning questions
    # such as "What does ADHD mean for my child at school?"
    patterns = (
        r"\b(?:am|are|is|do|does|could|would|can)\s+i\b(?:\s+\w+){0,5}\s+(?:have|be)\b",
        r"\b(?:do|does|could|would|can|is|are)\s+(?:he|she|they|we)\b(?:\s+\w+){0,5}\s+(?:have|be)\b",
        r"\b(?:does|could|would|can|is)\s+my\s+(?:child|son|daughter|partner|spouse|friend)\b(?:\s+\w+){0,5}\s+(?:have|be)\b",
        r"\b(?:do|does|could|would|can|is)\s+(?:the\s+)?patient\b(?:\s+\w+){0,5}\s+(?:have|be)\b",
    )
    return any(re.search(pattern, normalized) for pattern in patterns)


def _evidence_to_condition_inference(normalized: str, cfg: dict[str, Any]) -> bool:
    if not _has_evidence_subject(normalized, cfg) or not _has_condition(normalized, cfg):
        return False
    # Bare "mean" is permitted only in the evidence -> condition direction.
    evidence_pattern = r"(?:symptom|symptoms|trait|traits|sign|signs|behaviour|behavior|problems|answers|checklist|score|executive dysfunction|sensory overload)"
    condition_pattern = r"(?:autism|autistic|adhd|autism spectrum)"
    directional = (
        rf"\b{evidence_pattern}\b(?:\s+\w+){{0,5}}\s+mean(?:s)?\b(?:\s+\w+){{0,5}}\s+{condition_pattern}\b",
        rf"\b{evidence_pattern}\b(?:\s+\w+){{0,5}}\s+(?:point to|prove|show|qualify as|sound like|look)\b(?:\s+\w+){{0,5}}\s+{condition_pattern}\b",
        rf"\b{evidence_pattern}\b(?:\s+\w+){{0,5}}\s+(?:proof of)\b(?:\s+\w+){{0,5}}\s+{condition_pattern}\b",
    )
    return any(re.search(pattern, normalized) for pattern in directional)


def clinical_boundary(query: str) -> str | None:
    cfg = POLICY["clinical"]
    for clause in _clinical_clauses(query):
        normalized = _normalise(clause)
        if _has_any(normalized, cfg["negated_request_phrases"]):
            continue
        if not _has_condition(normalized, cfg):
            continue

        target = _has_person_target(normalized, cfg) or _has_deictic_target(normalized, cfg)
        if not target:
            continue

        if _direct_person_condition_question(normalized):
            return "clinical_diagnosis_boundary"
        if _evidence_to_condition_inference(normalized, cfg):
            return "clinical_diagnosis_boundary"
        if _has_any(normalized, cfg["diagnosis_request_phrases"]):
            return "clinical_diagnosis_boundary"
        if (_has_evidence_subject(normalized, cfg) or _has_deictic_target(normalized, cfg)) and _has_any(
            normalized, cfg["diagnosis_relation_phrases"]
        ):
            return "clinical_diagnosis_boundary"

    for clause in _clinical_clauses(query):
        normalized = _normalise(clause)
        if _has_any(normalized, cfg["negated_request_phrases"]):
            continue
        words = set(normalized.split())
        if not (words & set(cfg["medication_terms"])):
            continue
        if not _has_person_target(normalized, cfg):
            continue
        has_decision = _has_any(normalized, cfg["decision_cues"])
        has_action = bool(words & set(cfg["medication_action_terms"]))
        if has_decision and has_action:
            return "clinical_medication_boundary"
    return None


def requested_jurisdiction(query: str) -> tuple[list[str], bool]:
    cfg = POLICY["jurisdiction"]
    cleaned = re.sub(r"\bgov\s*\.\s*uk\b|\bgovuk\b|\bgov\s+uk\b", " ", query or "", flags=re.I)
    normalized = _normalise(cleaned)
    if not normalized:
        return [], False

    # Distinct jurisdictions attached to different life contexts are ambiguous
    # even when their union happens to equal a supported broad jurisdiction.
    nation_pattern = r"(northern ireland|england|scotland|wales)"
    context_pattern = "|".join(re.escape(term) for term in cfg["context_terms"])
    context_hits: list[str] = []
    forward = re.compile(
        rf"\b(?:{context_pattern})\b(?:\s+(?:in|to|from|within|the))?(?:\s+\w+){{0,4}}\s+{nation_pattern}\b"
    )
    reverse = re.compile(
        rf"\b{nation_pattern}\b(?:\s+\w+){{0,4}}\s+\b(?:{context_pattern})\b"
    )
    context_hits.extend(match.group(1) for match in forward.finditer(normalized))
    context_hits.extend(match.group(1) for match in reverse.finditer(normalized))
    if len(set(context_hits)) > 1:
        return [], True

    requested: set[str] = set()
    matched_sets: list[frozenset[str]] = []
    working = f" {normalized} "
    for alias in cfg["aliases"]:
        phrase = _normalise(alias["phrase"])
        padded = f" {phrase} "
        if padded in working:
            values = frozenset(cfg["scope_sets"][alias["scope"]])
            matched_sets.append(values)
            requested.update(values)
            working = working.replace(padded, " ")

    if not matched_sets:
        return [], False

    supported = {frozenset(values) for values in cfg["scope_sets"].values()}
    normalized_set = frozenset(requested)
    if normalized_set not in supported:
        return [], True

    return [name for name in cfg["canonical_order"] if name in requested], False


def _route_scope(route: str) -> list[str] | None:
    encoded = _SCOPE_BY_ROUTE.get(route)
    if not encoded:
        return None
    return list(POLICY["jurisdiction"]["scope_sets"][encoded["scope"]])


def _relevance(query: str, record: dict) -> dict[str, Any]:
    qnorm = _normalise(query)
    qmeaning = set(_meaningful_tokens(query))
    qcore = " ".join(_meaningful_tokens(query))
    aliases = list(record.get("aliases", []))
    intents = list(INTENT_PHRASES.get(record["route"], ()))

    reason = None
    for identity in [record["title"], *aliases]:
        if qnorm == _normalise(identity) or (qcore and qcore == " ".join(_meaningful_tokens(identity))):
            reason = "governed_identity"
            break

    if reason is None:
        for phrase in intents:
            pnorm = _normalise(phrase)
            if qnorm == pnorm or _has(qnorm, pnorm) or (qcore and qcore == " ".join(_meaningful_tokens(phrase))):
                reason = "routing_phrase"
                break

    # Editorial intent phrases can qualify only through the full routing-phrase
    # path above. Their individual words do not become governed identity anchors.
    identity_tokens = set(_meaningful_tokens(" ".join([record["title"], *aliases])))
    body_tokens = set(_meaningful_tokens(record["body"]))
    identity_anchors = sorted(qmeaning & identity_tokens)
    body_anchors = sorted(qmeaning & body_tokens)

    if reason is None:
        anchors = set(identity_anchors) | set(body_anchors)
        if (
            len(anchors) >= int(POLICY["eligibility"]["minimum_multi_anchors"])
            and (identity_anchors or not POLICY["eligibility"].get("require_identity_anchor_for_multi", True))
        ):
            reason = "multi_anchor"

    return {
        "eligible": reason is not None,
        "reason": reason,
        "identity_anchors": identity_anchors,
        "body_anchors": body_anchors,
    }


def _score(query: str, record: dict, relevance: dict[str, Any]) -> int:
    cfg = POLICY["ranking"]
    qnorm = _normalise(query)
    qtokens = set(_meaningful_tokens(query))
    aliases = list(record.get("aliases", []))
    intents = list(INTENT_PHRASES.get(record["route"], ()))

    score = {
        "governed_identity": int(cfg["identity_bonus"]),
        "routing_phrase": int(cfg["routing_phrase_bonus"]),
    }.get(relevance["reason"], 0)

    title_norm = _normalise(record["title"])
    body_norm = _normalise(record["body"])
    if qnorm == title_norm:
        score += int(cfg["title_exact_bonus"])
    elif qnorm and _has(title_norm, qnorm):
        score += int(cfg["title_contains_bonus"])
    if len(qtokens) >= 2 and qnorm and _has(body_norm, qnorm):
        score += int(cfg["body_contains_bonus"])

    identity_tokens = set(_meaningful_tokens(" ".join([record["title"], *aliases])))
    body_tokens = set(_meaningful_tokens(record["body"]))
    score += int(cfg["identity_token_weight"]) * len(qtokens & identity_tokens)
    score += int(cfg["body_token_weight"]) * len(qtokens & body_tokens)

    intent_tokens: set[str] = set()
    full_bonus = 0
    for phrase in intents:
        intent_tokens.update(_meaningful_tokens(phrase))
        pnorm = _normalise(phrase)
        if qnorm == pnorm or (pnorm and _has(qnorm, pnorm)):
            full_bonus = int(cfg["intent_full_bonus"])
    return score + full_bonus + int(cfg["intent_token_weight"]) * len(qtokens & intent_tokens)


def evaluate(
    query: str,
    *,
    limit: int = 5,
    index: list[dict] | None = None,
) -> tuple[dict[str, Any], list[SearchResult]]:
    records = build_index() if index is None else index
    _ensure_policy(records)
    normalized = _normalise(query)
    trace: dict[str, Any] = {
        "normalized_features": {
            "normalized": normalized,
            "tokens": _tokens(query),
            "meaningful_tokens": _meaningful_tokens(query),
        },
        "clinical_reason": None,
        "requested_scope": [],
        "jurisdiction_ambiguous": False,
        "records": [],
        "survivors": [],
        "orientation": "omitted",
        "ranking": [],
        "final_reason": "empty" if not normalized else None,
    }
    if not normalized:
        return trace, []

    trace["clinical_reason"] = clinical_boundary(query)
    if trace["clinical_reason"]:
        trace["final_reason"] = trace["clinical_reason"]
        return trace, []

    requested, ambiguous = requested_jurisdiction(query)
    trace["requested_scope"] = requested
    trace["jurisdiction_ambiguous"] = ambiguous
    if ambiguous:
        trace["final_reason"] = "jurisdiction_ambiguous"
        return trace, []

    survivors: list[tuple[dict, dict[str, Any]]] = []
    relevant_incompatible = False
    for record in records:
        relevance = _relevance(query, record)
        scope = _route_scope(record["route"])
        compatible = not requested or scope is None or set(requested).issubset(set(scope))
        if relevance["eligible"] and scope is not None and not compatible:
            relevant_incompatible = True
        trace["records"].append({
            "route": record["route"],
            "relevance": relevance,
            "scope": {"route_scope": scope, "compatible": compatible},
        })
        if relevance["eligible"] and compatible:
            survivors.append((record, relevance))

    trace["survivors"] = [record["route"] for record, _ in survivors]
    if not survivors:
        trace["final_reason"] = "jurisdiction_no_coverage" if relevant_incompatible else "no_match"
        return trace, []

    ranked = [
        (_score(query, record, relevance), record["kind"], _normalise(record["title"]), record["route"], record)
        for record, relevance in survivors
    ]
    ranked.sort(key=lambda row: (-row[0], row[1], row[2], row[3]))
    trace["ranking"] = [
        {"route": record["route"], "score": score, "tie_key": [kind, title, route]}
        for score, kind, title, route, record in ranked
    ]
    trace["final_reason"] = "results"
    results = [
        SearchResult(
            route=record["route"],
            kind=record["kind"],
            object_id=record["id"],
            title=record["title"],
            excerpt=record["body"][:220].strip(),
            score=score,
        )
        for score, _kind, _title, _route, record in ranked[:limit]
    ]
    return trace, results


def search(
    query: str,
    *,
    limit: int = 5,
    index: list[dict] | None = None,
) -> tuple[str, list[SearchResult]]:
    trace, results = evaluate(query, limit=limit, index=index)
    if trace["final_reason"] == "empty":
        return "empty", []
    return ("results", results) if results else ("no_answer", [])


def browser_index_json() -> str:
    records = build_index()
    _ensure_policy(records)
    index = [
        {
            **record,
            "intent": list(INTENT_PHRASES.get(record["route"], ())),
            "scope": _route_scope(record["route"]),
        }
        for record in records
    ]
    return json.dumps(
        {"policy": POLICY, "index": index},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run deterministic ND Oracle governed discovery.")
    parser.add_argument("query")
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()

    trace, results = evaluate(args.query)
    if args.trace:
        print(json.dumps(trace, indent=2, ensure_ascii=False))
    else:
        print("results" if results else ("empty" if trace["final_reason"] == "empty" else "no_answer"))
        for item in results:
            print(f"{item.score:3d} {item.route} {item.title}")
