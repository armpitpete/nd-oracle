# Ecosystem v0.6 test intent

Tests are intended to prove invariants, not implementation trivia.

Key invariants:

- authoritative Resource objects validate under the declared schema version;
- a Resource cannot validate without an access locator;
- active ecosystem routes exist only because reviewed resources exist;
- every Resource page exposes limitations, access/cost, conflicts and evidence status;
- a claimless listing explicitly avoids efficacy/safety claims;
- internal links and canonical/sitemap routes resolve;
- no new executable or data-collection surface is introduced;
- the existing topic evidence system remains intact.

Visual acceptance remains separate from objective tests.
