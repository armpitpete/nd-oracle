(() => {
  "use strict";

  const api = (() => {
    const norm = s => ((s || "").toLowerCase().match(/[a-z0-9]+/g) || []).join(" ");
    const has = (n, phrase) => {
      const p = norm(phrase);
      return !!p && ` ${n} `.includes(` ${p} `);
    };
    const uniqSorted = values => Array.from(new Set(values)).sort();
    const tokens = (s, policy) => {
      const stop = new Set(policy.normalization.stop_words);
      const min = Number(policy.normalization.minimum_token_length);
      return norm(s).split(" ").filter(t => t && !stop.has(t) && t.length >= min);
    };
    const meaningful = (s, policy) => {
      const generic = new Set(policy.normalization.generic_words);
      return tokens(s, policy).filter(t => !generic.has(t));
    };
    const intersects = (a, b) => {
      const bs = b instanceof Set ? b : new Set(b);
      return a.some(x => bs.has(x));
    };

    function clinicalBoundary(query, policy) {
      const c = policy.clinical;
      const stripped = (query || "").replace(/"[^"]*"|“[^”]*”/g, " ");
      const clauses = stripped.split(/[.!?;]+|\bbut\b/i).filter(x => norm(x));
      for (const clause of clauses) {
        const n = norm(clause);
        if (c.negated_request_phrases.some(p => has(n, p))) continue;
        const words = new Set(n.split(" "));
        if (
          intersects(c.condition_terms, words) &&
          (intersects(c.target_terms, words) || intersects(c.deictic_terms, words)) &&
          c.diagnosis_cues.some(cue => has(n, cue))
        ) return "clinical_diagnosis_boundary";
      }
      for (const clause of clauses) {
        const n = norm(clause);
        if (c.negated_request_phrases.some(p => has(n, p))) continue;
        const words = new Set(n.split(" "));
        if (
          intersects(c.medication_terms, words) &&
          intersects(c.target_terms, words) &&
          intersects(c.medication_action_terms, words) &&
          c.decision_cues.some(cue => has(n, cue))
        ) return "clinical_medication_boundary";
      }
      return null;
    }

    function requestedJurisdiction(query, policy) {
      const cfg = policy.jurisdiction;
      const n = norm((query || "").replace(/\bgov\s*\.\s*uk\b|\bgovuk\b|\bgov\s+uk\b/ig, " "));
      const relation = cfg.ambiguous_relation_terms.map(x => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|");
      const rx = new RegExp(`\\b(?:${relation})\\b(?:\\s+(?:in|to|from))?\\s+(northern ireland|england|scotland|wales)\\b`, "g");
      const hits = [];
      let match;
      while ((match = rx.exec(n)) !== null) hits.push(match[1]);
      if (new Set(hits).size > 1) return [[], true];
      const requested = new Set();
      let working = ` ${n} `;
      for (const alias of cfg.aliases) {
        const padded = ` ${norm(alias.phrase)} `;
        if (working.includes(padded)) {
          cfg.scope_sets[alias.scope].forEach(x => requested.add(x));
          working = working.split(padded).join(" ");
        }
      }
      return [cfg.canonical_order.filter(x => requested.has(x)), false];
    }

    function relevance(query, record, policy) {
      const qn = norm(query);
      const qmeaning = new Set(meaningful(query, policy));
      const qcore = meaningful(query, policy).join(" ");
      const aliases = record.aliases || [];
      const intents = policy.intent_phrases[record.route] || [];
      let reason = null;
      for (const identity of [record.title, ...aliases]) {
        if (qn === norm(identity) || (qcore && qcore === meaningful(identity, policy).join(" "))) {
          reason = "governed_identity";
          break;
        }
      }
      if (reason === null) {
        for (const phrase of intents) {
          const pn = norm(phrase);
          if (qn === pn || has(qn, pn) || (qcore && qcore === meaningful(phrase, policy).join(" "))) {
            reason = "routing_phrase";
            break;
          }
        }
      }
      const identityTokens = new Set(meaningful([record.title, ...aliases, ...intents].join(" "), policy));
      const bodyTokens = new Set(meaningful(record.body, policy));
      const identityAnchors = uniqSorted(Array.from(qmeaning).filter(x => identityTokens.has(x)));
      const bodyAnchors = uniqSorted(Array.from(qmeaning).filter(x => bodyTokens.has(x)));
      if (reason === null) {
        const anchors = new Set([...identityAnchors, ...bodyAnchors]);
        if (anchors.size >= Number(policy.eligibility.minimum_multi_anchors) && identityAnchors.length) {
          reason = "multi_anchor";
        }
      }
      return {eligible: reason !== null, reason, identity_anchors: identityAnchors, body_anchors: bodyAnchors};
    }

    function score(query, record, rel, policy) {
      const cfg = policy.ranking;
      const qn = norm(query);
      const qt = new Set(meaningful(query, policy));
      const aliases = record.aliases || [];
      const intents = policy.intent_phrases[record.route] || [];
      let s = rel.reason === "governed_identity" ? Number(cfg.identity_bonus)
        : rel.reason === "routing_phrase" ? Number(cfg.routing_phrase_bonus) : 0;
      const tn = norm(record.title), bn = norm(record.body);
      if (qn === tn) s += Number(cfg.title_exact_bonus);
      else if (qn && has(tn, qn)) s += Number(cfg.title_contains_bonus);
      if (qt.size >= 2 && qn && has(bn, qn)) s += Number(cfg.body_contains_bonus);
      const identityTokens = new Set(meaningful([record.title, ...aliases].join(" "), policy));
      const bodyTokens = new Set(meaningful(record.body, policy));
      s += Number(cfg.identity_token_weight) * Array.from(qt).filter(x => identityTokens.has(x)).length;
      s += Number(cfg.body_token_weight) * Array.from(qt).filter(x => bodyTokens.has(x)).length;
      const intentTokens = new Set();
      let full = 0;
      for (const phrase of intents) {
        meaningful(phrase, policy).forEach(x => intentTokens.add(x));
        const pn = norm(phrase);
        if (qn === pn || (pn && has(qn, pn))) full = Number(cfg.intent_full_bonus);
      }
      return s + full + Number(cfg.intent_token_weight) * Array.from(qt).filter(x => intentTokens.has(x)).length;
    }

    function compareRank(a, b) {
      if (a.score !== b.score) return b.score - a.score;
      for (const key of ["kind", "title_norm", "route"]) {
        if (a[key] < b[key]) return -1;
        if (a[key] > b[key]) return 1;
      }
      return 0;
    }

    function evaluate(query, payload, limit = 5) {
      const policy = payload.policy, index = payload.index;
      if (!policy || policy.version !== "1.1" || policy.orientation.enabled !== false) {
        throw new Error("Invalid v1.1 routing policy");
      }
      const normalized = norm(query);
      const trace = {
        normalized_features: {
          normalized,
          tokens: tokens(query, policy),
          meaningful_tokens: meaningful(query, policy),
        },
        clinical_reason: null,
        requested_scope: [],
        jurisdiction_ambiguous: false,
        records: [],
        survivors: [],
        orientation: "omitted",
        ranking: [],
        final_reason: normalized ? null : "empty",
      };
      if (!normalized) return {trace, results: []};

      trace.clinical_reason = clinicalBoundary(query, policy);
      if (trace.clinical_reason) {
        trace.final_reason = trace.clinical_reason;
        return {trace, results: []};
      }

      const [requested, ambiguous] = requestedJurisdiction(query, policy);
      trace.requested_scope = requested;
      trace.jurisdiction_ambiguous = ambiguous;
      if (ambiguous) {
        trace.final_reason = "jurisdiction_ambiguous";
        return {trace, results: []};
      }

      const survivors = [];
      let incompatible = false;
      for (const record of index) {
        const rel = relevance(query, record, policy);
        const scope = record.scope == null ? null : record.scope;
        const compatible = !requested.length || scope === null || requested.every(x => scope.includes(x));
        if (rel.eligible && scope !== null && !compatible) incompatible = true;
        trace.records.push({route: record.route, relevance: rel, scope: {route_scope: scope, compatible}});
        if (rel.eligible && compatible) survivors.push([record, rel]);
      }
      trace.survivors = survivors.map(x => x[0].route);
      if (!survivors.length) {
        trace.final_reason = incompatible ? "jurisdiction_no_coverage" : "no_match";
        return {trace, results: []};
      }

      const ranked = survivors.map(([record, rel]) => ({
        score: score(query, record, rel, policy),
        kind: record.kind,
        title_norm: norm(record.title),
        route: record.route,
        record,
      })).sort(compareRank);

      trace.ranking = ranked.map(x => ({
        route: x.route, score: x.score, tie_key: [x.kind, x.title_norm, x.route],
      }));
      trace.final_reason = "results";
      return {
        trace,
        results: ranked.slice(0, limit).map(x => ({
          route: x.record.route, kind: x.record.kind, object_id: x.record.id,
          title: x.record.title, excerpt: (x.record.body || "").slice(0, 220).trim(), score: x.score,
        })),
      };
    }
    return {evaluate, clinicalBoundary, requestedJurisdiction};
  })();

  if (typeof module !== "undefined" && module.exports) module.exports = api;

  if (typeof document !== "undefined") {
    const input = document.getElementById("find-input");
    const button = document.getElementById("find-button");
    const output = document.getElementById("find-results");
    const template = document.getElementById("search-index");
    if (input && button && output && template) {
      const payload = JSON.parse(template.content.textContent);
      const run = () => {
        const query = input.value.trim();
        output.replaceChildren();
        if (!query) {
          output.textContent = "Type a problem or question first.";
          return;
        }
        const {trace, results} = api.evaluate(query, payload, 5);
        if (trace.final_reason === "clinical_diagnosis_boundary" ||
            trace.final_reason === "clinical_medication_boundary") {
          output.innerHTML = '<h2>No governed answer</h2><p>ND Oracle cannot diagnose a person, choose medication or make an individual clinical decision. Try browsing <a href="/questions/">Questions</a> or <a href="/needs/">needs</a> instead.</p>';
          return;
        }
        if (!results.length) {
          const heading = trace.final_reason.startsWith("jurisdiction_") ? "No compatible governed route" : "No governed answer yet";
          output.innerHTML = `<h2>${heading}</h2><p>The current catalogue does not have a strong enough compatible route for that wording. Your query is not stored or sent to a search service. Try <a href="/needs/">browse by need</a>, <a href="/a-z/">A–Z</a>, or report a non-private content gap through <a href="/feedback/">feedback</a>.</p>`;
          return;
        }
        const h = document.createElement("h2");
        h.textContent = "Governed routes to inspect";
        output.appendChild(h);
        const note = document.createElement("p");
        note.className = "meta";
        note.textContent = "Ranked locally from reviewed ND Oracle content. Relevance is not recommendation.";
        output.appendChild(note);
        const list = document.createElement("ol");
        results.forEach(r => {
          const li = document.createElement("li");
          const a = document.createElement("a");
          a.href = r.route;
          a.textContent = r.title;
          li.appendChild(a);
          const m = document.createElement("span");
          m.className = "meta";
          m.textContent = ` ${r.kind}`;
          li.appendChild(m);
          list.appendChild(li);
        });
        output.appendChild(list);
      };
      button.addEventListener("click", run);
      input.addEventListener("keydown", e => {
        if (e.key === "Enter") {
          e.preventDefault();
          run();
        }
      });
    }
  }

  if (typeof process !== "undefined" && typeof require !== "undefined" && require.main === module) {
    const fs = require("fs");
    const input = JSON.parse(fs.readFileSync(0, "utf8"));
    const outputs = input.queries.map(q => api.evaluate(q, input.payload, input.limit || 5));
    process.stdout.write(JSON.stringify(outputs));
  }
})();
