# Singer 2016 Kindle full-date research

Status: **research only; date-representation decision required**

Prepared against protected `main`:

`622da858f5803be32f409a54f7e0c6742f19e373`

## Question

Can the already accepted Singer 2016 Kindle Evidence identity `neurodiversity-source-singer-2016-kindle` be represented faithfully under the v0.2 Evidence date requirement when the publication year is well supported but the exact publication day is not independently verified?

## Findings

The edition identity is strong. Judy Singer's own bibliography identifies *NeuroDiversity: The Birth of an Idea* as a 2016 Kindle publication and links the Amazon Kindle identity `B01HY0QTEE`. Singer's later bibliography repeats the same 2016 Kindle/ASIN identity.

The best day-level candidate comes from Goodreads, which records the matching title and author as a 98-page Kindle Edition published **July 3, 2016**.

Singer's contemporaneous launch post is dated **July 16, 2016** and says she had republished the thesis on Kindle with a new introduction. That independently establishes an upper bound consistent with July 3, but it does not state July 3 itself.

No conflicting day-level date tied to the 2016 Kindle identity was found. The 2017 print edition remains a distinct ISBN-bound identity and must not be used to fill or override the Kindle date.

## Evidence limits

Direct Amazon product metadata for ASIN `B01HY0QTEE` was not retrievable in this research environment. No first-party Singer statement giving the exact day and no independent library-catalogue day-level record for the 2016 Kindle edition was found.

Therefore **`2016-07-03` remains the best day-level candidate, but current evidence is insufficient to place it unqualified in the v0.2 `date` field.** Owner acceptance can decide how uncertainty is represented; it cannot convert uncertain metadata into a more certain fact.

The v0.2 Evidence schema currently requires an exact ISO date and has no date-precision or confidence mechanism. That creates a general modelling problem: an Evidence object whose publication year is known but whose exact day is unresolved cannot currently be represented without false precision or omission.

## Representation routes

Three routes remain open:

1. **Obtain stronger ASIN-bound day-level evidence.** Find first-party Amazon/KDP metadata, a first-party author record, or a strong catalogue/archive record tied specifically to `B01HY0QTEE` that establishes the exact day.
2. **Design a separately reviewed precision-aware date representation.** Preserve the known year while explicitly recording that month/day precision is unresolved, without weakening validation for genuinely exact dates.
3. **Retain the Singer 2016 edition unmapped.** Do not create the v0.2 Evidence object until its date can be represented faithfully under an accepted schema.

The preferred direction to investigate first is route 2 because incomplete bibliographic dates are likely to recur and the current schema cannot represent them honestly. This is a research direction only; it is not authority to change the schema.

## Recommendation

Do **not** accept `2016-07-03` as an unqualified full publication date on current evidence.

Recommended protected conclusion:

> `2016-07-03` remains the best day-level candidate, but current evidence is insufficient to place it unqualified in the v0.2 `date` field.

Resolve the date-representation question through a separately reviewed gate before deciding whether the Singer 2016 Evidence object can be mapped.

## Boundaries

This research does not authorise:

- authoritative v0.1 mutation;
- authoritative v0.2 replacement;
- acceptance of `2016-07-03` as an exact publication fact;
- a Singer 2017 identity or date change;
- claim-text changes;
- any new Evidence Contribution role or binding;
- schema or validator changes;
- ADHD migration or semantic disposition;
- publication or deployment.

## Reopening conditions

Reopen the day-level evidence assessment if ASIN-bound Amazon/KDP metadata, a first-party author record, or a stronger contemporaneous catalogue/archival record tied to the same Kindle identity establishes or conflicts with `2016-07-03`.

Reopen the representation decision if a separately reviewed precision-aware date design provides a faithful way to encode the known year without asserting unsupported day-level precision.
