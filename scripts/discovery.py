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

# Compatibility export only; v1.1 boundary authority is clinical_boundary().
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
    return [t for t in _normalise(value).split() if t not in STOP_WORDS and len(t) >= minimum]

def _meaningful_tokens(value: str) -> list[str]:
    return [t for t in _tokens(value) if t not in GENERIC_WORDS]

def _load_dir(name: str) -> list[dict]:
    directory = OBJECTS / name
    if not directory.is_dir():
        return []
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(directory.glob("*.json"))]

def build_index() -> list[dict]:
    records = []
    for item in _load_dir("questions"):
        records.append({
            "route": f"/questions/{item['id']}/", "kind": "Question", "id": item["id"],
            "title": item["question"], "aliases": [],
            "body": " ".join([item.get("why_it_matters", ""), item.get("current_understanding", ""),
                              *item.get("evidence_needed", []), *item.get("dissent", [])]),
        })
    for item in _load_dir("concepts"):
        aliases = list(item.get("aliases", []))
        records.append({
            "route": f"/understand/{item['id']}/", "kind": "Topic", "id": item["id"],
            "title": item["name"], "aliases": aliases,
            "body": " ".join([item.get("summary", ""), " ".join(aliases),
                              " ".join(c.get("text", "") for c in item.get("claims", []))]),
        })
    for item in _load_dir("resources"):
        records.append({
            "route": f"/resources/{item['id']}/", "kind": "Resource", "id": item["id"],
            "title": item["name"], "aliases": [],
            "body": " ".join([item.get("description", ""), item.get("intended_use", ""),
                              item.get("audience_or_context", ""), *item.get("limitations", []),
                              *item.get("cost_or_access_notes", [])]),
        })
    return sorted(records, key=lambda r: (r["kind"], _normalise(r["title"]), r["route"]))

def _blob_sha(payload: bytes) -> str:
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()

def validate_policy(*, policy: dict[str, Any] | None = None, index: list[dict] | None = None) -> None:
    candidate = POLICY if policy is None else policy
    if candidate.get("version") != "1.1":
        raise ValueError("Routing policy must be v1.1")
    expected = {
        "England": {"England"}, "Scotland": {"Scotland"}, "Wales": {"Wales"},
        "Northern Ireland": {"Northern Ireland"}, "Great Britain": {"England", "Scotland", "Wales"},
        "England and Wales": {"England", "Wales"},
        "United Kingdom": {"England", "Scotland", "Wales", "Northern Ireland"},
    }
    scopes = candidate["jurisdiction"]["scope_sets"]
    if {k: set(v) for k, v in scopes.items()} != expected:
        raise ValueError("Jurisdiction scope sets do not match frozen v1.1")
    if set(candidate["jurisdiction"]["canonical_order"]) != {"England","Scotland","Wales","Northern Ireland"}:
        raise ValueError("Jurisdiction canonical order is incomplete")
    provenance = candidate["scope_provenance"]
    if provenance.get("basis") != "entire governed object blob; any object drift invalidates routing scope":
        raise ValueError("Unexpected scope provenance basis")
    if provenance.get("source_path_rule") != "objects/{route_kind}/{route_id}.json":
        raise ValueError("Unexpected scope provenance path rule")
    entries = provenance["routes"]
    if len(entries) != 29:
        raise ValueError(f"Expected 29 frozen scoped routes, found {len(entries)}")
    indexed = {r["route"] for r in (build_index() if index is None else index)}
    for route, encoded in entries.items():
        if not isinstance(encoded, list) or len(encoded) != 2:
            raise ValueError(f"Malformed scope entry: {route}")
        scope, expected_sha = encoded
        if route not in indexed or scope not in scopes:
            raise ValueError(f"Invalid scoped route: {route}")
        parts = route.strip("/").split("/")
        if len(parts) != 2 or parts[0] not in {"questions", "resources"}:
            raise ValueError(f"Unresolvable scope source: {route}")
        source = ROOT / "objects" / parts[0] / f"{parts[1]}.json"
        if not source.is_file() or _blob_sha(source.read_bytes()) != expected_sha:
            raise ValueError(f"Scope provenance fingerprint mismatch: {route}")
        if json.loads(source.read_text(encoding="utf-8")).get("id") != parts[1]:
            raise ValueError(f"Scope provenance identity mismatch: {route}")
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

def clinical_boundary(query: str) -> str | None:
    cfg = POLICY["clinical"]
    stripped = re.sub(r'"[^"]*"|“[^”]*”', " ", query or "")
    clauses = [c for c in re.split(r"[.!?;]+|\bbut\b", stripped, flags=re.I) if _normalise(c)]
    for clause in clauses:
        n = _normalise(clause)
        if any(_has(n, p) for p in cfg["negated_request_phrases"]):
            continue
        words = set(n.split())
        if (words & set(cfg["condition_terms"])
                and (words & set(cfg["target_terms"]) or words & set(cfg["deictic_terms"]))
                and any(_has(n, cue) for cue in cfg["diagnosis_cues"])):
            return "clinical_diagnosis_boundary"
    for clause in clauses:
        n = _normalise(clause)
        if any(_has(n, p) for p in cfg["negated_request_phrases"]):
            continue
        words = set(n.split())
        if (words & set(cfg["medication_terms"]) and words & set(cfg["target_terms"])
                and words & set(cfg["medication_action_terms"])
                and any(_has(n, cue) for cue in cfg["decision_cues"])):
            return "clinical_medication_boundary"
    return None

def requested_jurisdiction(query: str) -> tuple[list[str], bool]:
    cfg = POLICY["jurisdiction"]
    n = _normalise(re.sub(r"\bgov\s*\.\s*uk\b|\bgovuk\b|\bgov\s+uk\b", " ", query or "", flags=re.I))
    relations = "|".join(re.escape(x) for x in cfg["ambiguous_relation_terms"])
    hits = re.findall(rf"\b(?:{relations})\b(?:\s+(?:in|to|from))?\s+(northern ireland|england|scotland|wales)\b", n)
    if len(set(hits)) > 1:
        return [], True
    requested, working = set(), f" {n} "
    for alias in cfg["aliases"]:
        padded = f" {_normalise(alias['phrase'])} "
        if padded in working:
            requested.update(cfg["scope_sets"][alias["scope"]])
            working = working.replace(padded, " ")
    return [x for x in cfg["canonical_order"] if x in requested], False

def _route_scope(route: str) -> list[str] | None:
    encoded = _SCOPE_BY_ROUTE.get(route)
    return list(POLICY["jurisdiction"]["scope_sets"][encoded[0]]) if encoded else None

def _relevance(query: str, record: dict) -> dict[str, Any]:
    qn, qmeaning = _normalise(query), set(_meaningful_tokens(query))
    qcore = " ".join(_meaningful_tokens(query))
    aliases, intents = list(record.get("aliases", [])), list(INTENT_PHRASES.get(record["route"], ()))
    reason = None
    for identity in [record["title"], *aliases]:
        if qn == _normalise(identity) or (qcore and qcore == " ".join(_meaningful_tokens(identity))):
            reason = "governed_identity"
            break
    if reason is None:
        for phrase in intents:
            pn = _normalise(phrase)
            if qn == pn or _has(qn, pn) or (qcore and qcore == " ".join(_meaningful_tokens(phrase))):
                reason = "routing_phrase"
                break
    identity_tokens = set(_meaningful_tokens(" ".join([record["title"], *aliases, *intents])))
    body_tokens = set(_meaningful_tokens(record["body"]))
    identity_anchors = sorted(qmeaning & identity_tokens)
    body_anchors = sorted(qmeaning & body_tokens)
    if reason is None:
        anchors = set(identity_anchors) | set(body_anchors)
        if len(anchors) >= int(POLICY["eligibility"]["minimum_multi_anchors"]) and identity_anchors:
            reason = "multi_anchor"
    return {"eligible": reason is not None, "reason": reason,
            "identity_anchors": identity_anchors, "body_anchors": body_anchors}

def _score(query: str, record: dict, relevance: dict[str, Any]) -> int:
    cfg, qn = POLICY["ranking"], _normalise(query)
    qtokens = set(_meaningful_tokens(query))
    aliases, intents = list(record.get("aliases", [])), list(INTENT_PHRASES.get(record["route"], ()))
    score = {"governed_identity": int(cfg["identity_bonus"]),
             "routing_phrase": int(cfg["routing_phrase_bonus"])}.get(relevance["reason"], 0)
    tn, bn = _normalise(record["title"]), _normalise(record["body"])
    if qn == tn:
        score += int(cfg["title_exact_bonus"])
    elif qn and _has(tn, qn):
        score += int(cfg["title_contains_bonus"])
    if len(qtokens) >= 2 and qn and _has(bn, qn):
        score += int(cfg["body_contains_bonus"])
    score += int(cfg["identity_token_weight"]) * len(qtokens & set(_meaningful_tokens(" ".join([record["title"], *aliases]))))
    score += int(cfg["body_token_weight"]) * len(qtokens & set(_meaningful_tokens(record["body"])))
    intent_tokens, full = set(), 0
    for phrase in intents:
        intent_tokens.update(_meaningful_tokens(phrase))
        pn = _normalise(phrase)
        if qn == pn or (pn and _has(qn, pn)):
            full = int(cfg["intent_full_bonus"])
    return score + full + int(cfg["intent_token_weight"]) * len(qtokens & intent_tokens)

def evaluate(query: str, *, limit: int = 5, index: list[dict] | None = None) -> tuple[dict[str, Any], list[SearchResult]]:
    records = build_index() if index is None else index
    _ensure_policy(records)
    normalized = _normalise(query)
    trace: dict[str, Any] = {
        "normalized_features": {"normalized": normalized, "tokens": _tokens(query),
                                "meaningful_tokens": _meaningful_tokens(query)},
        "clinical_reason": None, "requested_scope": [], "jurisdiction_ambiguous": False,
        "records": [], "survivors": [], "orientation": "omitted", "ranking": [],
        "final_reason": "empty" if not normalized else None,
    }
    if not normalized:
        return trace, []
    trace["clinical_reason"] = clinical_boundary(query)
    if trace["clinical_reason"]:
        trace["final_reason"] = trace["clinical_reason"]
        return trace, []
    requested, ambiguous = requested_jurisdiction(query)
    trace["requested_scope"], trace["jurisdiction_ambiguous"] = requested, ambiguous
    if ambiguous:
        trace["final_reason"] = "jurisdiction_ambiguous"
        return trace, []
    survivors, incompatible = [], False
    for record in records:
        relevance, scope = _relevance(query, record), _route_scope(record["route"])
        compatible = not requested or scope is None or set(requested).issubset(set(scope))
        incompatible = incompatible or (relevance["eligible"] and scope is not None and not compatible)
        trace["records"].append({"route": record["route"], "relevance": relevance,
                                 "scope": {"route_scope": scope, "compatible": compatible}})
        if relevance["eligible"] and compatible:
            survivors.append((record, relevance))
    trace["survivors"] = [r["route"] for r, _ in survivors]
    if not survivors:
        trace["final_reason"] = "jurisdiction_no_coverage" if incompatible else "no_match"
        return trace, []
    ranked = [(_score(query, r, rel), r["kind"], _normalise(r["title"]), r["route"], r)
              for r, rel in survivors]
    ranked.sort(key=lambda x: (-x[0], x[1], x[2], x[3]))
    trace["ranking"] = [{"route": r["route"], "score": score, "tie_key": [kind, title, route]}
                        for score, kind, title, route, r in ranked]
    trace["final_reason"] = "results"
    results = [SearchResult(r["route"], r["kind"], r["id"], r["title"], r["body"][:220].strip(), score)
               for score, _kind, _title, _route, r in ranked[:limit]]
    return trace, results

def search(query: str, *, limit: int = 5, index: list[dict] | None = None) -> tuple[str, list[SearchResult]]:
    trace, results = evaluate(query, limit=limit, index=index)
    if trace["final_reason"] == "empty":
        return "empty", []
    return ("results", results) if results else ("no_answer", [])

def browser_index_json() -> str:
    records = build_index()
    _ensure_policy(records)
    index = [{**r, "intent": list(INTENT_PHRASES.get(r["route"], ())), "scope": _route_scope(r["route"])}
             for r in records]
    return json.dumps({"policy": POLICY, "index": index}, ensure_ascii=False,
                      separators=(",", ":")).replace("</", "<\\/")

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
