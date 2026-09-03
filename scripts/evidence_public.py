from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlsplit


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _safe_https(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    return value


def _load_objects(root: Path) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for path in sorted((root / "objects").glob("*/*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("id"):
            records[str(obj["id"])] = obj
    return records


def _claim_href(owner_type: str, owner_id: str, claim_id: str) -> str:
    base = "understand" if owner_type == "concept" else "resources"
    return f"/{base}/{owner_id}/#claim-{claim_id}"


def build_projections(root: Path) -> list[dict]:
    objects = _load_objects(root)
    projections: list[dict] = []

    for owner_id, obj in sorted(objects.items()):
        if obj.get("schema_version") != "0.1" or obj.get("type") != "concept":
            continue
        claim_map = {str(claim.get("id")): claim for claim in obj.get("claims", [])}
        uncertainty_map = {str(item.get("id")): item for item in obj.get("uncertainties", [])}
        for source in obj.get("sources", []):
            source_id = str(source.get("id"))
            claims = []
            for claim_id, claim in claim_map.items():
                if source_id not in claim.get("source_ids", []):
                    continue
                uncertainties = [
                    uncertainty_map[item_id].get("question")
                    for item_id in claim.get("uncertainty_ids", [])
                    if item_id in uncertainty_map
                ]
                claims.append({
                    "claim_ref": f"{owner_id}#{claim_id}",
                    "claim_id": claim_id,
                    "owner_id": owner_id,
                    "owner_type": "concept",
                    "owner_name": obj.get("name", owner_id),
                    "claim_text": claim.get("text", ""),
                    "confidence": claim.get("confidence"),
                    "href": _claim_href("concept", owner_id, claim_id),
                    "role": None,
                    "finding": None,
                    "population_or_context": None,
                    "methodology": None,
                    "limitations": [],
                    "uncertainties": [value for value in uncertainties if value],
                })
            public_id = f"legacy-{owner_id}-{source_id}"
            locator = None
            if source.get("url"):
                locator = {"type": "url", "value": source.get("url")}
            elif source.get("doi"):
                locator = {"type": "doi", "value": source.get("doi")}
            projections.append({
                "public_id": public_id,
                "route": f"/evidence/{public_id}/",
                "evidence_model": "legacy_v0.1_embedded",
                "source_id": source_id,
                "evidence_id": None,
                "title": source.get("citation") or source_id,
                "citation": source.get("citation") or source_id,
                "source_kind": source.get("kind") or "other",
                "authorship": source.get("authorship"),
                "date": source.get("date"),
                "date_precision": source.get("date_precision"),
                "accessed": source.get("accessed"),
                "last_reviewed": obj.get("provenance", {}).get("last_reviewed"),
                "locator": locator,
                "owner_id": owner_id,
                "owner_type": "concept",
                "owner_name": obj.get("name", owner_id),
                "claims": claims,
                "conflicts_of_interest": source.get("conflicts_of_interest", []),
                "funding": source.get("funding"),
                "provenance_method": obj.get("provenance", {}).get("method"),
            })

    for evidence_id, evidence in sorted(objects.items()):
        if evidence.get("schema_version") != "0.2" or evidence.get("type") != "evidence":
            continue
        claims = []
        for contribution in evidence.get("contributions", []):
            claim_ref = str(contribution.get("claim_ref", ""))
            if "#" not in claim_ref:
                continue
            owner_id, claim_id = claim_ref.split("#", 1)
            owner = objects.get(owner_id, {})
            claim = next((item for item in owner.get("claims", []) if item.get("id") == claim_id), {})
            uncertainties = [item.get("text") for item in claim.get("uncertainties", []) if item.get("text")]
            claims.append({
                "claim_ref": claim_ref,
                "claim_id": claim_id,
                "owner_id": owner_id,
                "owner_type": owner.get("type", "resource"),
                "owner_name": owner.get("name") or owner.get("title") or owner_id,
                "claim_text": claim.get("text", claim_ref),
                "confidence": claim.get("confidence"),
                "href": _claim_href(str(owner.get("type", "resource")), owner_id, claim_id),
                "role": contribution.get("role"),
                "finding": contribution.get("finding"),
                "population_or_context": contribution.get("population_or_context"),
                "methodology": contribution.get("methodology"),
                "limitations": [item.get("text", "") if isinstance(item, dict) else str(item) for item in contribution.get("limitations", [])],
                "uncertainties": uncertainties,
            })
        projections.append({
            "public_id": evidence_id,
            "route": f"/evidence/{evidence_id}/",
            "evidence_model": "normalized_v0.2",
            "source_id": None,
            "evidence_id": evidence_id,
            "title": evidence.get("title") or evidence.get("citation") or evidence_id,
            "citation": evidence.get("citation") or evidence.get("title") or evidence_id,
            "source_kind": evidence.get("source_kind") or "other",
            "authorship": evidence.get("authorship"),
            "date": evidence.get("date"),
            "date_precision": evidence.get("date_precision"),
            "accessed": evidence.get("accessed"),
            "last_reviewed": evidence.get("provenance", {}).get("last_reviewed"),
            "locator": evidence.get("locator"),
            "owner_id": None,
            "owner_type": None,
            "owner_name": None,
            "claims": claims,
            "conflicts_of_interest": evidence.get("conflicts_of_interest", []),
            "funding": evidence.get("funding"),
            "provenance_method": evidence.get("provenance", {}).get("method"),
        })

    projections.sort(key=lambda item: (str(item["title"]).casefold(), item["public_id"]))
    public_ids = [item["public_id"] for item in projections]
    routes = [item["route"] for item in projections]
    if len(public_ids) != len(set(public_ids)) or len(routes) != len(set(routes)):
        raise ValueError("Evidence projection IDs/routes must be unique")
    return projections


def _locator_html(locator: object) -> str:
    if not isinstance(locator, dict):
        return '<p class="meta">No public locator recorded.</p>'
    locator_type = str(locator.get("type", "other"))
    value = locator.get("value")
    if locator_type == "url":
        safe = _safe_https(value)
        if safe:
            return f'<p><a href="{_esc(safe)}" rel="noopener noreferrer">Open source</a></p>'
        return '<p class="meta">No safe HTTPS locator recorded.</p>'
    if locator_type == "doi" and isinstance(value, str):
        safe = _safe_https(f"https://doi.org/{value}")
        if safe:
            return f'<p>DOI: <a href="{_esc(safe)}" rel="noopener noreferrer">{_esc(value)}</a></p>'
    return f'<p>{_esc(locator_type.upper())}: {_esc(value or "Not recorded")}</p>'


def _list(values: list[object]) -> str:
    cleaned = [str(value) for value in values if value not in {None, ""}]
    if not cleaned:
        return '<p class="meta">None recorded.</p>'
    return '<ul>' + ''.join(f'<li>{_esc(value)}</li>' for value in cleaned) + '</ul>'


def render_index(projections: list[dict], *, page_shell) -> str:
    counts: dict[str, int] = {}
    for item in projections:
        kind = str(item.get("source_kind") or "other")
        counts[kind] = counts.get(kind, 0) + 1
    rows = []
    for item in projections:
        searchable = " ".join([
            str(item.get("title") or ""), str(item.get("citation") or ""), str(item.get("authorship") or ""),
            str(item.get("source_kind") or ""), str(item.get("owner_name") or ""),
            " ".join(str(claim.get("claim_text") or "") for claim in item.get("claims", [])),
            str((item.get("locator") or {}).get("value") or ""),
        ]).casefold()
        rows.append(
            f'<article class="resource-row evidence-row" data-evidence-row data-search="{_esc(searchable)}">'
            f'<h2><a href="{_esc(item["route"])}">{_esc(item["title"])}</a></h2>'
            f'<p>{_esc(item["citation"])}</p>'
            f'<p class="meta">Kind: {_esc(str(item.get("source_kind") or "other").replace("_", " "))} · '
            f'Model: {_esc("normalized v0.2" if item["evidence_model"] == "normalized_v0.2" else "accepted legacy v0.1")}</p>'
            '</article>'
        )
    summary = ', '.join(f'{kind.replace("_", " ")}: {count}' for kind, count in sorted(counts.items()))
    body = f'''
<section class="notice"><strong>Evidence is not proof and source count is not a vote.</strong> Each record is shown only for the exact governed claim routes it bears on, with uncertainty and limitations kept visible.</section>
<section aria-labelledby="evidence-search-heading">
  <h2 id="evidence-search-heading">Find an Evidence record</h2>
  <label for="evidence-query">Search citation, author, source kind, identifier, topic or exact claim wording</label>
  <input id="evidence-query" type="search" autocomplete="off" spellcheck="false">
  <p id="evidence-search-status" class="meta" aria-live="polite">Showing all {len(projections)} governed source records.</p>
</section>
<section aria-labelledby="evidence-corpus-heading"><h2 id="evidence-corpus-heading">Current governed evidence corpus</h2><p class="meta">{_esc(summary)}</p><div id="evidence-results">{''.join(rows)}</div></section>
<section><h2>How to read these records</h2><p>The catalogue projects both accepted v0.1 embedded sources and normalized v0.2 Evidence objects. A legacy source is not silently assigned a v0.2 contribution role. Official, peer-reviewed, community and lived-experience sources each remain limited to what they can support for an exact claim.</p></section>
'''
    page = page_shell(
        "Evidence",
        "Inspect the governed sources behind ND Oracle claims without turning citations into scores, endorsements or automatic conclusions.",
        body,
        current=None,
        path="/evidence/",
    )
    return page.replace('</body>', '\n</body>', 1)


def render_detail(item: dict, *, page_shell) -> str:
    model = "Normalized v0.2 Evidence" if item["evidence_model"] == "normalized_v0.2" else "Accepted legacy v0.1 embedded source"
    metadata = [
        f'<li><strong>Source kind:</strong> {_esc(str(item.get("source_kind") or "other").replace("_", " "))}</li>',
        f'<li><strong>Evidence model:</strong> {_esc(model)}</li>',
    ]
    if item.get("authorship"):
        metadata.append(f'<li><strong>Authorship:</strong> {_esc(item["authorship"])}</li>')
    if item.get("date"):
        precision = f' ({item.get("date_precision")})' if item.get("date_precision") else ''
        metadata.append(f'<li><strong>Source date:</strong> {_esc(item["date"])}{_esc(precision)}</li>')
    if item.get("accessed"):
        metadata.append(f'<li><strong>Accessed:</strong> {_esc(item["accessed"])}</li>')
    if item.get("last_reviewed"):
        metadata.append(f'<li><strong>Oracle last reviewed:</strong> {_esc(item["last_reviewed"])}</li>')

    claim_rows = []
    for claim in item.get("claims", []):
        role = (
            str(claim.get("role")).replace("_", " ")
            if claim.get("role")
            else "Legacy source route — no v0.2 contribution role inferred"
        )
        finding = f'<p><strong>Finding used here:</strong> {_esc(claim["finding"])}</p>' if claim.get("finding") else ''
        context = f'<p><strong>Population/context:</strong> {_esc(claim["population_or_context"])}</p>' if claim.get("population_or_context") else ''
        method = f'<p><strong>Method:</strong> {_esc(claim["methodology"])}</p>' if claim.get("methodology") else ''
        claim_rows.append(f'''
<article class="claim-card">
  <h3><a href="{_esc(claim["href"])}">{_esc(claim["claim_text"])}</a></h3>
  <p class="meta">Claim reference: {_esc(claim["claim_ref"])} · Confidence: {_esc(claim.get("confidence") or "not recorded")} · Evidence role: {_esc(role)}</p>
  {finding}{context}{method}
  <div><strong>Evidence limitations</strong>{_list(claim.get("limitations", []))}</div>
  <div><strong>Claim uncertainty</strong>{_list(claim.get("uncertainties", []))}</div>
</article>''')
    if not claim_rows:
        claim_rows.append('<p class="meta">No governed claim contribution is recorded. This should be treated as an audit defect, not evidence of general relevance.</p>')

    conflicts = item.get("conflicts_of_interest") or []
    if isinstance(conflicts, str):
        conflicts = [conflicts]
    funding = item.get("funding")
    body = f'''
<p class="back-link"><a href="/evidence/">← All Evidence</a></p>
<section class="notice"><strong>A source is not a conclusion.</strong> Read the exact claim, role, context, limitations and uncertainty together. This record is not a recommendation, diagnosis, legal decision or quality score.</section>
<section aria-labelledby="source-heading"><h2 id="source-heading">Source record</h2><p>{_esc(item["citation"])}</p><ul>{''.join(metadata)}</ul>{_locator_html(item.get("locator"))}</section>
<section aria-labelledby="claims-heading"><h2 id="claims-heading">Claims this source bears on</h2>{''.join(claim_rows)}</section>
<section aria-labelledby="conflicts-heading"><h2 id="conflicts-heading">Funding and conflicts</h2>{_list(([f"Funding: {funding}"] if funding else []) + list(conflicts))}</section>
<details class="provenance"><summary>Evidence projection provenance</summary><p>{_esc(item.get("provenance_method") or "Projected deterministically from the authoritative repository record without changing the source or claim semantics.")}</p><p class="meta">Public projection ID: {_esc(item["public_id"])}</p></details>
'''
    return page_shell(
        str(item["title"]),
        "A governed Evidence source projected for the exact ND Oracle claims it bears on.",
        body,
        current=None,
        path=item["route"],
    )


EVIDENCE_SEARCH_JS = r'''(() => {
  const input = document.getElementById('evidence-query');
  const rows = Array.from(document.querySelectorAll('[data-evidence-row]'));
  const status = document.getElementById('evidence-search-status');
  if (!input || !status) return;
  const normalise = value => value.toLocaleLowerCase().trim().replace(/\s+/g, ' ');
  const apply = () => {
    const query = normalise(input.value);
    let shown = 0;
    for (const row of rows) {
      const haystack = normalise(row.dataset.search || '');
      const visible = !query || query.split(' ').every(token => haystack.includes(token));
      row.hidden = !visible;
      if (visible) shown += 1;
    }
    status.textContent = query ? `${shown} matching Evidence record${shown === 1 ? '' : 's'}.` : `Showing all ${rows.length} governed source records.`;
  };
  input.addEventListener('input', apply);
})();
'''


def write_evidence_routes(destination: Path, projections: list[dict], *, page_shell) -> None:
    index = destination / "evidence" / "index.html"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(render_index(projections, page_shell=page_shell), encoding="utf-8")
    for item in projections:
        target = destination / item["route"].strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_detail(item, page_shell=page_shell), encoding="utf-8")
    (destination / "evidence-find.js").write_text(EVIDENCE_SEARCH_JS, encoding="utf-8")


def inject_claim_links(destination: Path, projections: list[dict]) -> None:
    for item in projections:
        link = f'<p class="meta"><a href="{_esc(item["route"])}">Open canonical Evidence record</a></p>'
        if item["evidence_model"] == "legacy_v0.1_embedded":
            page_path = destination / "understand" / str(item["owner_id"]) / "index.html"
            if not page_path.is_file():
                raise ValueError(f"Missing public owner page for {item['public_id']}")
            page = page_path.read_text(encoding="utf-8")
            marker = f'<article class="source" id="source-{_esc(item["source_id"])}">'
            if marker not in page:
                raise ValueError(f"Cannot locate legacy source card {item['public_id']}")
            if item["route"] not in page:
                page = page.replace(marker, marker + link, 1)
                page_path.write_text(page, encoding="utf-8")
            continue

        owner_ids = sorted({claim["owner_id"] for claim in item.get("claims", [])})
        for owner_id in owner_ids:
            owner_type = next(claim["owner_type"] for claim in item["claims"] if claim["owner_id"] == owner_id)
            folder = "understand" if owner_type == "concept" else "resources"
            page_path = destination / folder / owner_id / "index.html"
            if not page_path.is_file():
                raise ValueError(f"Missing public claim-owner page for {item['public_id']}: {owner_id}")
            page = page_path.read_text(encoding="utf-8")
            title_marker = f'<article class="evidence-card"><h4>{_esc(item["title"])}</h4>'
            if title_marker not in page:
                raise ValueError(f"Cannot locate normalized Evidence card {item['public_id']} in {owner_id}")
            if item["route"] not in page:
                page = page.replace(title_marker, title_marker + link)
                page_path.write_text(page, encoding="utf-8")


def route_markers(projections: list[dict]) -> list[tuple[str, str]]:
    return [("/evidence/", "<h1>Evidence</h1>")] + [
        (item["route"], f'<h1>{_esc(item["title"])}</h1>') for item in projections
    ]
