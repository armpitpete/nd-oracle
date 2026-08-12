# Foundation seed source snapshots — 2026-08-10

These files are immutable byte-for-byte snapshots of the original five authoritative v0.1 concept objects before the Batch B evidence review.

They exist so historical migration proofs remain anchored to the exact source objects and blob SHAs they originally evaluated even after the live authoritative corpus evolves.

Rules:

- Do not edit these snapshots in place.
- Historical migration builders, fixtures and tests that assert the old blob identities must read these snapshots rather than the living `objects/concepts/` files.
- Current validation, site generation and new review work must continue to read the living authoritative corpus.
- A future historical source state requires a new snapshot directory, never mutation of this one.

Frozen blobs:

- `autism.json` — `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`
- `neurodiversity.json` — `5a38bc4250079412dd3f4da1d598dfcab984ca66`
- `adhd.json` — `719f26a9af773cd1bcf670df4d12ed5f6bcf0a23`
- `executive-function.json` — `f67e1a73e89245f9e6c6c2a34d4acc47169b8273`
- `sensory-processing.json` — `7626d61a2844aae88ce6811760dfe97b5baa94bc`
