# Post-baseline NHS bulletin ingest — 4 September 2026

Status: **partially promoted**

Promotion state on 4 September 2026:

- learning-disability register / annual health checks: **promoted into the active-corpus candidate**;
- person-centred suicide safety: **promoted into the active-corpus candidate**;
- autistic school attendance: **held in the candidate layer until the exact current Autism Central destination is resolved**.

Accepted production remains unchanged at 319 governed objects / 403 canonical routes. The active-corpus promotion candidate is 323 objects / 407 routes and requires its own protected merge before it reaches `main`.

This pack records three bounded ND Oracle additions selected from NHS England's 4 September 2026 Mental Health, Learning Disability and Neurodevelopmental Conditions bulletin.

It deliberately does **not** alter accepted production. After PR #148, accepted production is the Ireland Assessment & diagnosis v1 release recorded by `contracts/current-production.json`: **319 governed objects and 403 canonical public routes**.

## Candidate additions

1. **Learning disability register / annual health checks — England**
   - NHS England's September 2026 primary-care identification guidance.
   - Register inclusion may be made in primary care where learning disability is clinically indicated without requiring specialist confirmation or a completed formal diagnostic assessment.
   - Register identification is not itself a formal diagnosis and does not establish eligibility for specialist learning-disability services.
   - The register supports proactive primary care including annual health checks for eligible people aged 14+, vaccinations and reasonable adjustments.

2. **Autistic school-attendance difficulties — England**
   - NHS England's 4 September 2026 bulletin summarises Autism Central guidance.
   - It frames attendance difficulty as potentially connected to anxiety, sensory overwhelm, communication differences, bullying or peer difficulties, and masking-related burnout rather than simply unwillingness to attend.
   - The support framing includes looking for patterns and early signs, responding with curiosity rather than blame, working with SENCo or pastoral staff, involving the child, using visual/written communication and considering smaller steps where full attendance is not yet manageable.
   - The exact current Autism Central destination linked by the bulletin must be resolved before promotion. No substitute article URL is invented in this pack.

3. **Person-centred suicide safety — England**
   - NHS England's Staying Safe from Suicide guidance is treated as policy/practice framing.
   - It moves away from simplistic prediction and static low/medium/high risk labels toward therapeutic engagement, shared formulation, dynamic review and collaborative safety planning.
   - It must never become individual suicide-risk assessment, crisis counselling or a replacement for the existing urgent mental-health signpost.

## Promotion boundary

Promotion requires explicit source re-checking, active-schema validation, route-count reconciliation, hostile safety review and the normal exact-head protected merge process.

The current production pointer remains authoritative until a separate deployment and live verification.
