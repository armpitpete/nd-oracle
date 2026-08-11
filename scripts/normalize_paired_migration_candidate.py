#!/usr/bin/env python3
"""Fold accepted D1-D17 decisions into the paired non-authoritative candidate."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "migration-candidates" / "autism-neurodiversity"
AUT_FIX = ROOT / "tests" / "fixtures" / "migration" / "autism"
AUT = ROOT / "objects" / "concepts" / "autism.json"
ND = ROOT / "objects" / "concepts" / "neurodiversity.json"
D1 = "d1-neurobiology-citation-correction"
D7 = "d7-autism-who-perspective-framing"
D8 = "d8-neurodiversity-botha-citation-correction"
D9 = "d9-neurodiversity-collective-perspective-framing"
D10 = "d10-neurodiversity-paradigm-perspective-framing"
D11 = "d11-singer-edition-identity-preservation"
D12 = "d12-singer-2017-date-enrichment"
D13 = "d13-singer-edition-specific-contribution-bindings"
D14 = "d14-singer-2016-claim2-binding-followup"
D16 = "d16-embedded-uncertainty-schema-implementation"
D17 = "d17-neurodiversity-legacy-structural-disposition"
S16 = "neurodiversity-source-singer-2016-kindle"
S17 = "neurodiversity-source-singer-2017-revised-print"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def payload(unit: str):
    return json.loads(unit.split(":", 1)[1])


def unit(prefix: str, value: dict) -> str:
    return prefix + ":" + json.dumps(value, sort_keys=True, separators=(",", ":"))


def decisions():
    a = load(AUT_FIX / "owner-decisions.json")["decisions"]
    b = load(MIG / "owner-decisions.json")["decisions"]
    merged = {x["id"]: copy.deepcopy(x) for x in a}
    merged.update({x["id"]: copy.deepcopy(x) for x in b})
    return merged


def prov():
    return {
        "created": "2026-08-11",
        "created_by": "ND Oracle migration candidate builder",
        "method": "Non-authoritative assembly from anchored v0.1 sources, verified enrichment, and accepted owner decisions.",
        "review_state": "unreviewed_seed",
        "last_reviewed": None,
    }


def unc(x):
    return {
        "id": x["id"], "text": x["question"], "why_it_matters": x["why_it_matters"],
        "reopening_or_reduction_conditions": list(x["what_would_reduce_it"]), "status": x["status"],
    }


def contrib(eid, cid, x, role=None):
    owner = cid.split("-claim-", 1)[0]
    return {
        "id": f"{eid}-{cid}-contribution", "claim_ref": f"{owner}#{cid}", "role": role or x["role"],
        "finding": x["finding"], "population_or_context": x["population_or_context"],
        "methodology": x["methodology"], "limitations": [],
    }


def evidence(eid, kind, citation, url, date, date_precision, accessed, authorship, title, contributions):
    return {
        "schema_version": "0.2", "id": eid, "type": "evidence", "status": "seed", "provenance": prov(),
        "title": title, "source_kind": kind, "citation": citation, "locator": {"type": "url", "value": url},
        "date": date, "date_precision": date_precision, "accessed": accessed, "authorship": authorship,
        "contributions": contributions,
    }


def perspective(old, accepted, evidence_ids):
    return {
        "schema_version": "0.2", "id": old["id"], "type": "perspective", "status": "seed", "provenance": prov(),
        "held_by": {"name": old["held_by"], "scope": accepted["held_by.scope"]}, "position": old["summary"],
        "reasoning": accepted["reasoning"],
        "supporting_material_refs": [{"type": "evidence", "id": x} for x in evidence_ids],
        "disagreement_refs": [], "scope": accepted["scope"],
    }


def bundle(eid, target, trigger, value, routes, origin="verified_evidence", note="D1-D17 normalized assembly"):
    return {
        "id": eid, "target_field": target, "trigger_unit": trigger, "proposed_value": value,
        "evidence_route": list(routes), "value_origin": origin, "supplied_by": note,
        "review_state": "verified", "limitations": [],
    }


def pending_date(trigger, routes):
    return {
        "id": "enrich-neurodiversity-source-singer-2016-kindle-date",
        "target_field": f"evidence:{S16}.date", "trigger_unit": trigger, "proposed_value": None,
        "evidence_route": list(routes), "value_origin": "pending",
        "supplied_by": "Singer 2016 date research after D11-D14; authoritative acceptance not implied.",
        "review_state": "pending",
        "limitations": ["2016-07-03 remains secondary-catalogue evidence and is not owner-accepted."],
    }


def build_objects(a, n, ds, a_enrich, n_research, singer):
    ae = {x["id"]: x for x in a_enrich["entries"]}
    av = lambda i: ae[i]["proposed_value"]
    asrc = {x["id"]: x for x in a["sources"]}
    who, neuro = asrc["autism-source-who"], asrc["autism-source-neurobiology"]
    who_fields = lambda cid: {
        k: av(f"enrich-autism-source-who-{cid}-{k.replace('_','-')}")
        for k in ("role", "finding", "population_or_context", "methodology")
    }
    who_obj = evidence(
        who["id"], who["kind"], who["citation"], who["url"], av("enrich-autism-source-who-date"), "day",
        who["accessed"], av("enrich-autism-source-who-authorship"), av("enrich-autism-source-who-title"),
        [
            contrib(who["id"], "autism-claim-1", who_fields("autism-claim-1")),
            contrib(who["id"], "autism-claim-2", who_fields("autism-claim-2")),
        ],
    )
    nf = {
        k: av(f"enrich-autism-source-neurobiology-autism-claim-2-{k.replace('_','-')}")
        for k in ("role", "finding", "population_or_context", "methodology")
    }
    neuro_obj = evidence(
        neuro["id"], neuro["kind"], ds[D1]["accepted_value"], neuro["url"],
        av("enrich-autism-source-neurobiology-date"), "day", neuro["accessed"],
        av("enrich-autism-source-neurobiology-authorship"), av("enrich-autism-source-neurobiology-title"),
        [contrib(neuro["id"], "autism-claim-2", nf)],
    )
    au = {x["id"]: x for x in a["uncertainties"]}
    amap = {"autism-claim-1": [who["id"]], "autism-claim-2": [who["id"], neuro["id"]]}
    aconcept = {
        "schema_version": "0.2", "id": "autism", "type": "concept", "status": a["status"],
        "provenance": copy.deepcopy(a["provenance"]), "name": a["name"], "aliases": list(a["aliases"]),
        "summary": a["summary"], "scope": copy.deepcopy(a["scope"]),
        "claims": [
            {
                "id": c["id"], "text": c["text"], "confidence": c["confidence"],
                "evidence_ids": amap[c["id"]], "uncertainties": [unc(au[x]) for x in c["uncertainty_ids"]],
                "question_ids": [],
            }
            for c in a["claims"]
        ],
        "relations": [], "question_ids": [],
    }
    ap = perspective(a["perspectives"][0], ds[D7]["accepted_fields"], [who["id"]])

    nsrc = {x["id"]: x for x in n["sources"]}
    npers = {x["id"]: x for x in n["perspectives"]}
    br = n_research["sources"]["neurodiversity-source-botha"]
    bs = nsrc["neurodiversity-source-botha"]
    botha = evidence(
        bs["id"], bs["kind"], ds[D8]["accepted_citation"], bs["url"], br["metadata"]["date"]["value"], "day",
        bs["accessed"], br["metadata"]["authorship"]["value"], br["metadata"]["title"]["value"],
        [contrib(bs["id"], "neurodiversity-claim-1", br["contributions"]["neurodiversity-claim-1"])],
    )
    ids = {x["id"]: x for x in singer["candidates"]}
    sr = n_research["sources"]["neurodiversity-source-singer"]
    ss = nsrc["neurodiversity-source-singer"]
    i17 = ids[S17]
    cs = []
    for cid in ("neurodiversity-claim-1", "neurodiversity-claim-2"):
        b = next(x for x in i17["accepted_contribution_bindings"] if x["claim_ref"].endswith("#" + cid))
        cs.append(contrib(S17, cid, sr["contributions"][cid], b["role"]))
    singer17 = evidence(
        S17, ss["kind"], "Singer, Judy. NeuroDiversity: The Birth of an Idea. Revised print edition (2017).",
        ss["url"], ds[D12]["accepted_full_publication_date"], "day", ss["accessed"], i17["authorship"],
        i17["title"], cs,
    )
    nu = {x["id"]: x for x in n["uncertainties"]}
    nmap = {"neurodiversity-claim-1": [S17, bs["id"]], "neurodiversity-claim-2": [S17]}
    nconcept = {
        "schema_version": "0.2", "id": "neurodiversity", "type": "concept", "status": n["status"],
        "provenance": copy.deepcopy(n["provenance"]), "name": n["name"], "aliases": list(n["aliases"]),
        "summary": n["summary"], "scope": copy.deepcopy(n["scope"]),
        "claims": [
            {
                "id": c["id"], "text": c["text"], "confidence": c["confidence"],
                "evidence_ids": nmap[c["id"]], "uncertainties": [unc(nu[x]) for x in c["uncertainty_ids"]],
                "question_ids": [],
            }
            for c in n["claims"]
        ],
        "relations": [], "question_ids": [],
    }
    pcollect = perspective(npers["neurodiversity-perspective-collective"], ds[D9]["accepted_fields"], [bs["id"]])
    ppar = perspective(npers["neurodiversity-perspective-paradigm"], ds[D10]["accepted_fields"], [S17])
    objects = {x["id"]: x for x in (aconcept, who_obj, neuro_obj, ap, nconcept, botha, singer17, pcollect, ppar)}
    return objects, ids[S16]


def normalize_preservation(entries):
    out = []
    for old in entries:
        x = copy.deepcopy(old)
        oid = x["source_object_id"]
        u = x["unit"]
        for k in (
            "candidate_destination", "enrichment_ref", "owner_decision_ref", "dependency_ref", "unresolved_reason",
            "legacy_value", "rejection_reason", "reopening_condition",
        ):
            x.pop(k, None)
        if u.startswith("source:"):
            s = payload(u)
            if oid == "autism":
                ref = f"enrich-{s['id']}-object"
            elif s["id"] == "neurodiversity-source-botha":
                ref = "enrich-neurodiversity-source-botha-object"
            else:
                ref = "enrich-neurodiversity-source-singer-identity-split"
            x.update(
                disposition="represented_with_verified_enrichment", enrichment_ref=ref,
                candidate_destination="normalized v0.2 evidence candidate or accepted split identity",
            )
        elif u.startswith("perspective:"):
            p = payload(u)
            x.update(
                disposition="represented_with_verified_enrichment", enrichment_ref=f"enrich-{p['id']}-object",
                candidate_destination=f"candidate/perspectives/{p['id']}.json",
            )
        elif u.startswith("uncertainty:") or u.startswith("claim-uncertainty-route:"):
            x.update(
                disposition="represented_exactly", owner_decision_ref=D16,
                candidate_destination=f"candidate/concepts/{oid}.json embedded uncertainty",
            )
        elif u.startswith("claim-source-route:") and oid == "neurodiversity" and u.endswith("->neurodiversity-source-singer"):
            cid = u.split(":", 1)[1].split("->", 1)[0]
            x.update(
                disposition="represented_with_verified_enrichment",
                enrichment_ref=f"enrich-neurodiversity-source-singer-{cid}-bindings",
                candidate_destination=f"candidate/concepts/neurodiversity.json claim {cid}",
            )
        elif u.startswith("relation:"):
            r = payload(u)
            if (oid, r.get("target_id")) in {("autism", "neurodiversity"), ("neurodiversity", "autism")}:
                x.update(
                    disposition="legacy_retained_unmapped", owner_decision_ref=D17, legacy_value=r,
                    unresolved_reason="D17 preserves this exact legacy record without emitting a v0.2 taxonomy edge.",
                )
            elif oid == "neurodiversity" and r.get("target_id") == "adhd":
                x.update(
                    disposition="structural_dependency", dependency_ref="dependency-neurodiversity-adhd",
                    unresolved_reason="Separate Neurodiversity↔ADHD semantic disposition remains unaccepted.",
                )
            else:
                x = copy.deepcopy(old)
        else:
            x = copy.deepcopy(old)
        x["source_object_id"] = oid
        out.append(x)
    return out


def apply_normalization(destination: Path) -> Path:
    a, n, ds = load(AUT), load(ND), decisions()
    ae = load(AUT_FIX / "enrichment-ledger.json")
    nr = load(MIG / "neurodiversity-enrichment-research.json")
    singer = load(MIG / "singer-edition-candidates.json")
    objects, singer16 = build_objects(a, n, ds, ae, nr, singer)
    manifest = load(destination / "manifest.json")
    manifest["candidate_object_ids"] = sorted(objects)
    manifest["package_status"] = "enrichment_pending"
    write(destination / "manifest.json", manifest)
    pres = load(destination / "preservation-ledger.json")
    pres["entries"] = normalize_preservation(pres["entries"])
    write(destination / "preservation-ledger.json", pres)

    enrichments = []
    for e in ae["entries"]:
        if e["review_state"] == "verified":
            enrichments.append(copy.deepcopy(e))
    for objid in ("autism-source-who", "autism-source-neurobiology", "autism-perspective-clinical"):
        routes = ds[D7]["evidence_route"] if objid == "autism-perspective-clinical" else [
            next(s["url"] for s in a["sources"] if s["id"] == objid)
        ]
        origin = "owner_decision" if objid in {"autism-source-neurobiology", "autism-perspective-clinical"} else "verified_evidence"
        enrichments.append(
            bundle(f"enrich-{objid}-object", f"candidate:{objid}", objid, objects[objid], routes, origin)
        )
    bs = next(s for s in n["sources"] if s["id"] == "neurodiversity-source-botha")
    enrichments.append(
        bundle(
            "enrich-neurodiversity-source-botha-object", "candidate:neurodiversity-source-botha", unit("source", bs),
            objects[bs["id"]], ds[D8]["evidence_route"], "owner_decision",
        )
    )
    ss = next(s for s in n["sources"] if s["id"] == "neurodiversity-source-singer")
    strig = unit("source", ss)
    ids = {x["id"]: x for x in singer["candidates"]}
    enrichments.append(
        bundle(
            "enrich-neurodiversity-source-singer-identity-split", "evidence identity split", strig,
            {"evidence_ids": [S16, S17]}, ids[S16]["evidence_routes"], "owner_decision",
        )
    )
    enrichments.append(pending_date(strig, ids[S16]["evidence_routes"]))
    enrichments.append(
        bundle(
            f"enrich-{S17}-object", f"candidate:{S17}", strig, objects[S17],
            ids[S17]["evidence_routes"], "owner_decision",
        )
    )
    for cid in ("neurodiversity-claim-1", "neurodiversity-claim-2"):
        bindings = []
        for sid in (S16, S17):
            b = next(x for x in ids[sid]["accepted_contribution_bindings"] if x["claim_ref"].endswith("#" + cid))
            bindings.append({"evidence_id": sid, "role": b["role"], "decision_ref": b["decision_ref"]})
        enrichments.append(
            bundle(
                f"enrich-neurodiversity-source-singer-{cid}-bindings", f"claim:{cid}.evidence bindings",
                f"claim-source-route:{cid}->neurodiversity-source-singer", bindings,
                ids[S17]["evidence_routes"], "owner_decision",
            )
        )
    for pid, did in (
        ("neurodiversity-perspective-collective", D9),
        ("neurodiversity-perspective-paradigm", D10),
    ):
        enrichments.append(
            bundle(f"enrich-{pid}-object", f"candidate:{pid}", pid, objects[pid], ds[did]["evidence_route"], "owner_decision")
        )
    write(destination / "enrichment-ledger.json", {"migration_contract_version": "0.2", "entries": enrichments})

    candidate = destination / "candidate"
    old = candidate / "structural-pair.json"
    if old.exists():
        old.unlink()
    for obj in objects.values():
        folder = {"concept": "concepts", "evidence": "evidence", "perspective": "perspectives"}[obj["type"]]
        write(candidate / folder / f"{obj['id']}.json", obj)
    write(
        destination / "pending-evidence-identities.json",
        {"entries": [{"id": S16, "accepted_identity": singer16, "blocking_field": "date"}]},
    )
    write(destination / "migration-state.json", load(MIG / "migration-state.json"))
    log = (destination / "decision-log.md").read_text(encoding="utf-8")
    log += "\n\n## D1-D17 state normalization — 2026-08-11\n\nAccepted D1-D17 work is folded into schema-shaped non-authoritative candidate objects. Exactly two blockers remain: Singer 2016 full date and the separate Neurodiversity↔ADHD semantic dependency. The package remains `enrichment_pending`; authoritative replacement is not authorised.\n"
    (destination / "decision-log.md").write_text(log, encoding="utf-8")
    return destination
