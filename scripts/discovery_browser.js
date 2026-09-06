(() => {
  "use strict";

  const api = (() => {
    const norm = value => ((value || "").toLowerCase().match(/[a-z0-9]+/g) || []).join(" ");
    const has = (normalized, phrase) => {
      const needle = norm(phrase);
      return !!needle && ` ${normalized} `.includes(` ${needle} `);
    };
    const hasAny = (normalized, phrases) => phrases.some(phrase => has(normalized, phrase));
    const uniqSorted = values => Array.from(new Set(values)).sort();
    const escapeRegex = value => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

    const tokens = (value, policy) => {
      const stop = new Set(policy.normalization.stop_words);
      const minimum = Number(policy.normalization.minimum_token_length);
      return norm(value).split(" ").filter(token => token && !stop.has(token) && token.length >= minimum);
    };

    const meaningful = (value, policy) => {
      const generic = new Set(policy.normalization.generic_words);
      return tokens(value, policy).filter(token => !generic.has(token));
    };

    const intersects = (values, candidate) => {
      const other = candidate instanceof Set ? candidate : new Set(candidate);
      return values.some(value => other.has(value));
    };

    const clinicalClauses = query => {
      const stripped = (query || "").replace(/"[^"]*"|“[^”]*”/g, " ");
      return stripped.split(/[.!?;]+|\bbut\b/i).filter(clause => norm(clause));
    };

    const hasPersonTarget = (normalized, cfg) => intersects(cfg.target_terms, new Set(normalized.split(" ")));
    const hasDeicticTarget = (normalized, cfg) => intersects(cfg.deictic_terms, new Set(normalized.split(" ")));
    const hasCondition = (normalized, cfg) => intersects(cfg.condition_terms, new Set(normalized.split(" ")));
    const hasEvidenceSubject = (normalized, cfg) => hasAny(normalized, cfg.evidence_terms);

    function directPersonConditionQuestion(normalized) {
      const patterns = [
        /\b(?:am|are|is|do|does|could|would|can)\s+i\b(?:\s+\w+){0,5}\s+(?:have|be)\b/,
        /\b(?:do|does|could|would|can|is|are)\s+(?:he|she|they|we)\b(?:\s+\w+){0,5}\s+(?:have|be)\b/,
        /\b(?:does|could|would|can|is)\s+my\s+(?:child|son|daughter|partner|spouse|friend)\b(?:\s+\w+){0,5}\s+(?:have|be)\b/,
        /\b(?:do|does|could|would|can|is)\s+(?:the\s+)?patient\b(?:\s+\w+){0,5}\s+(?:have|be)\b/,
      ];
      return patterns.some(pattern => pattern.test(normalized));
    }

    function evidenceToConditionInference(normalized, cfg) {
      if (!hasEvidenceSubject(normalized, cfg) || !hasCondition(normalized, cfg)) return false;
      const evidence = "(?:symptom|symptoms|trait|traits|sign|signs|behaviour|behavior|problems|answers|checklist|score|executive dysfunction|sensory overload)";
      const condition = "(?:autism|autistic|adhd|autism spectrum)";
      const patterns = [
        new RegExp(`\\b${evidence}\\b(?:\\s+\\w+){0,5}\\s+mean(?:s)?\\b(?:\\s+\\w+){0,5}\\s+${condition}\\b`),
        new RegExp(`\\b${evidence}\\b(?:\\s+\\w+){0,5}\\s+(?:point to|prove|show|qualify as|sound like|look)\\b(?:\\s+\\w+){0,5}\\s+${condition}\\b`),
        new RegExp(`\\b${evidence}\\b(?:\\s+\\w+){0,5}\\s+(?:proof of)\\b(?:\\s+\\w+){0,5}\\s+${condition}\\b`),
      ];
      return patterns.some(pattern => pattern.test(normalized));
    }

    function clinicalBoundary(query, policy) {
      const cfg = policy.clinical;
      for (const clause of clinicalClauses(query)) {
        const normalized = norm(clause);
        if (hasAny(normalized, cfg.negated_request_phrases)) continue;
        if (!hasCondition(normalized, cfg)) continue;

        const target = hasPersonTarget(normalized, cfg) || hasDeicticTarget(normalized, cfg);
        if (!target) continue;

        if (directPersonConditionQuestion(normalized)) return "clinical_diagnosis_boundary";
        if (evidenceToConditionInference(normalized, cfg)) return "clinical_diagnosis_boundary";
        if (hasAny(normalized, cfg.diagnosis_request_phrases)) return "clinical_diagnosis_boundary";
        if (
          (hasEvidenceSubject(normalized, cfg) || hasDeicticTarget(normalized, cfg)) &&
          hasAny(normalized, cfg.diagnosis_relation_phrases)
        ) return "clinical_diagnosis_boundary";
      }

      for (const clause of clinicalClauses(query)) {
        const normalized = norm(clause);
        if (hasAny(normalized, cfg.negated_request_phrases)) continue;
        const words = new Set(normalized.split(" "));
        if (!intersects(cfg.medication_terms, words)) continue;
        if (!hasPersonTarget(normalized, cfg)) continue;
        const hasDecision = hasAny(normalized, cfg.decision_cues);
        const hasAction = intersects(cfg.medication_action_terms, words);
        if (hasDecision && hasAction) return "clinical_medication_boundary";
      }
      return null;
    }

    function requestedJurisdiction(query, policy) {
      const cfg = policy.jurisdiction;
      const cleaned = (query || "").replace(/\bgov\s*\.\s*uk\b|\bgovuk\b|\bgov\s+uk\b/ig, " ");
      const normalized = norm(cleaned);
      if (!normalized) return [[], false];

      const nationPattern = "(northern ireland|republic of ireland|england|scotland|wales|ireland)";
      const contextPattern = cfg.context_terms.map(escapeRegex).join("|");
      const forward = new RegExp(
        `\\b(?:${contextPattern})\\b(?:\\s+(?:in|to|from|within|the))?(?:\\s+\\w+){0,4}\\s+${nationPattern}\\b`,
        "g"
      );
      const reverse = new RegExp(
        `\\b${nationPattern}\\b(?:\\s+\\w+){0,4}\\s+\\b(?:${contextPattern})\\b`,
        "g"
      );
      const contextHits = [];
      let match;
      while ((match = forward.exec(normalized)) !== null) contextHits.push(match[1]);
      while ((match = reverse.exec(normalized)) !== null) contextHits.push(match[1]);
      if (new Set(contextHits).size > 1) return [[], true];

      const requested = new Set();
      const matchedSets = [];
      let working = ` ${normalized} `;
      for (const alias of cfg.aliases) {
        const phrase = norm(alias.phrase);
        const padded = ` ${phrase} `;
        if (working.includes(padded)) {
          const values = cfg.scope_sets[alias.scope];
          matchedSets.push(new Set(values));
          values.forEach(value => requested.add(value));
          working = working.split(padded).join(" ");
        }
      }
      if (!matchedSets.length) return [[], false];

      const signature = values => Array.from(values).sort().join("|");
      const supported = new Set(Object.values(cfg.scope_sets).map(values => signature(values)));
      if (!supported.has(signature(requested))) return [[], true];

      return [cfg.canonical_order.filter(value => requested.has(value)), false];
    }

    function relevance(query, record, policy) {
      const qnorm = norm(query);
      const qmeaning = new Set(meaningful(query, policy));
      const qcore = meaningful(query, policy).join(" ");
      const aliases = record.aliases || [];
      const intents = policy.intent_phrases[record.route] || [];
      let reason = null;

      for (const identity of [record.title, ...aliases]) {
        if (qnorm === norm(identity) || (qcore && qcore === meaningful(identity, policy).join(" "))) {
          reason = "governed_identity";
          break;
        }
      }

      if (reason === null) {
        for (const phrase of intents) {
          const pnorm = norm(phrase);
          if (
            qnorm === pnorm ||
            has(qnorm, pnorm) ||
            (qcore && qcore === meaningful(phrase, policy).join(" "))
          ) {
            reason = "routing_phrase";
            break;
          }
        }
      }

      const identityTokens = new Set(meaningful([record.title, ...aliases].join(" "), policy));
      const bodyTokens = new Set(meaningful(record.body, policy));
      const identityAnchors = uniqSorted(Array.from(qmeaning).filter(token => identityTokens.has(token)));
      const bodyAnchors = uniqSorted(Array.from(qmeaning).filter(token => bodyTokens.has(token)));

      if (reason === null) {
        const anchors = new Set([...identityAnchors, ...bodyAnchors]);
        if (
          anchors.size >= Number(policy.eligibility.minimum_multi_anchors) &&
          (identityAnchors.length || !policy.eligibility.require_identity_anchor_for_multi)
        ) reason = "multi_anchor";
      }

      return {
        eligible: reason !== null,
        reason,
        identity_anchors: identityAnchors,
        body_anchors: bodyAnchors,
      };
    }

    function score(query, record, rel, policy) {
      const cfg = policy.ranking;
      const qnorm = norm(query);
      const queryTokens = new Set(meaningful(query, policy));
      const aliases = record.aliases || [];
      const intents = policy.intent_phrases[record.route] || [];

      let value = rel.reason === "governed_identity"
        ? Number(cfg.identity_bonus)
        : rel.reason === "routing_phrase"
          ? Number(cfg.routing_phrase_bonus)
          : 0;

      const titleNorm = norm(record.title);
      const bodyNorm = norm(record.body);
      if (qnorm === titleNorm) value += Number(cfg.title_exact_bonus);
      else if (qnorm && has(titleNorm, qnorm)) value += Number(cfg.title_contains_bonus);
      if (queryTokens.size >= 2 && qnorm && has(bodyNorm, qnorm)) value += Number(cfg.body_contains_bonus);

      const identityTokens = new Set(meaningful([record.title, ...aliases].join(" "), policy));
      const bodyTokens = new Set(meaningful(record.body, policy));
      value += Number(cfg.identity_token_weight) * Array.from(queryTokens).filter(token => identityTokens.has(token)).length;
      value += Number(cfg.body_token_weight) * Array.from(queryTokens).filter(token => bodyTokens.has(token)).length;

      const intentTokens = new Set();
      let fullBonus = 0;
      for (const phrase of intents) {
        meaningful(phrase, policy).forEach(token => intentTokens.add(token));
        const pnorm = norm(phrase);
        if (qnorm === pnorm || (pnorm && has(qnorm, pnorm))) fullBonus = Number(cfg.intent_full_bonus);
      }
      return value + fullBonus +
        Number(cfg.intent_token_weight) * Array.from(queryTokens).filter(token => intentTokens.has(token)).length;
    }

    function compareRank(left, right) {
      if (left.score !== right.score) return right.score - left.score;
      for (const key of ["kind", "title_norm", "route"]) {
        if (left[key] < right[key]) return -1;
        if (left[key] > right[key]) return 1;
      }
      return 0;
    }

    function evaluate(query, payload, limit = 5) {
      const policy = payload.policy;
      const index = payload.index;
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
      let relevantIncompatible = false;
      for (const record of index) {
        const rel = relevance(query, record, policy);
        const scope = record.scope == null ? null : record.scope;
        const compatible = !requested.length || scope === null || requested.every(value => scope.includes(value));
        if (rel.eligible && scope !== null && !compatible) relevantIncompatible = true;
        trace.records.push({
          route: record.route,
          relevance: rel,
          scope: {route_scope: scope, compatible},
        });
        if (rel.eligible && compatible) survivors.push([record, rel]);
      }

      trace.survivors = survivors.map(([record]) => record.route);
      if (!survivors.length) {
        trace.final_reason = relevantIncompatible ? "jurisdiction_no_coverage" : "no_match";
        return {trace, results: []};
      }

      const ranked = survivors.map(([record, rel]) => ({
        score: score(query, record, rel, policy),
        kind: record.kind,
        title_norm: norm(record.title),
        route: record.route,
        record,
      })).sort(compareRank);

      trace.ranking = ranked.map(row => ({
        route: row.route,
        score: row.score,
        tie_key: [row.kind, row.title_norm, row.route],
      }));
      trace.final_reason = "results";

      return {
        trace,
        results: ranked.slice(0, limit).map(row => ({
          route: row.record.route,
          kind: row.record.kind,
          object_id: row.record.id,
          title: row.record.title,
          excerpt: (row.record.body || "").slice(0, 220).trim(),
          score: row.score,
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
        if (
          trace.final_reason === "clinical_diagnosis_boundary" ||
          trace.final_reason === "clinical_medication_boundary"
        ) {
          output.innerHTML = '<h2>No governed answer</h2><p>ND Oracle cannot diagnose you or another person, choose medication or make an individual clinical decision. Try browsing <a href="/questions/">Questions</a> or <a href="/needs/">needs</a> instead.</p>';
          return;
        }

        if (!results.length) {
          const heading = trace.final_reason.startsWith("jurisdiction_")
            ? "No compatible governed route"
            : "No governed answer yet";
          output.innerHTML = `<h2>${heading}</h2><p>The current catalogue does not have a strong enough compatible route for that wording. Your query is not stored or sent to a search service. Try <a href="/needs/">browse by need</a>, <a href="/a-z/">A–Z</a>, or report a non-private content gap through <a href="/feedback/">feedback</a>.</p>`;
          return;
        }

        const heading = document.createElement("h2");
        heading.textContent = "Governed routes to inspect";
        output.appendChild(heading);

        const note = document.createElement("p");
        note.className = "meta";
        note.textContent = "Ranked locally from reviewed ND Oracle content. Relevance is not recommendation.";
        output.appendChild(note);

        const recordsByRoute = new Map(payload.index.map(record => [record.route, record]));
        const list = document.createElement("ol");
        results.forEach(result => {
          const item = document.createElement("li");
          const link = document.createElement("a");
          link.href = result.route;
          link.textContent = result.title;
          item.appendChild(link);

          const metadata = document.createElement("span");
          metadata.className = "result-metadata";

          const kind = document.createElement("span");
          kind.className = "semantic-badge";
          kind.textContent = result.kind;
          metadata.appendChild(kind);

          const record = recordsByRoute.get(result.route);
          if (record && Array.isArray(record.scope) && record.scope.length) {
            const scope = document.createElement("span");
            scope.className = "scope-badge";
            scope.textContent = record.scope.join(", ");
            metadata.appendChild(scope);
          }

          item.appendChild(metadata);
          list.appendChild(item);
        });
        output.appendChild(list);
      };

      button.addEventListener("click", run);
      input.addEventListener("keydown", event => {
        if (event.key === "Enter") {
          event.preventDefault();
          run();
        }
      });
    }
  }

  if (
    typeof process !== "undefined" &&
    typeof require !== "undefined" &&
    require.main === module
  ) {
    const fs = require("fs");
    const input = JSON.parse(fs.readFileSync(0, "utf8"));
    const outputs = input.queries.map(query => api.evaluate(query, input.payload, input.limit || 5));
    process.stdout.write(JSON.stringify(outputs));
  }
})();
