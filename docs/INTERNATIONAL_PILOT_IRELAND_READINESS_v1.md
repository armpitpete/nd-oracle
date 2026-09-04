# International pilot source-readiness probe — Republic of Ireland v1

Date: 2026-09-04
Status: readiness candidate
Parent architecture: `docs/INTERNATIONAL_EXPANSION_ARCHITECTURE_v1.md`

## Decision

**Recommend the Republic of Ireland as ND Oracle's first non-UK jurisdiction pilot.**

Do not create a broad Ireland corpus yet. The first implementation should be a bounded **Assessment & diagnosis** reference slice, using the UK Assessment model as precedent while preserving Irish service geography, law, terminology and current implementation gaps.

The pilot is source-ready because Ireland has:

- current HSE national autism assessment information;
- a national HSE Autism Assessment and Intervention Pathway Protocol effective from 25 March 2026;
- a maintained HSE Adult ADHD Model of Care, updated June 2026;
- explicit evidence that adult ADHD public-service implementation varies by area;
- clear HSE Children's Disability Network Team and primary-care referral routes;
- a legally distinct Assessment of Need process under the Disability Act 2005;
- six current HSE Health Regions with explicit local decision-making responsibility.

It is also architecturally valuable because the Republic of Ireland directly borders Northern Ireland. This gives ND Oracle a high-value hostile boundary: **Republic-of-Ireland HSE routes must never inherit Northern Ireland HSC/NHS rules, and Northern Ireland routes must never inherit Republic-of-Ireland HSE rules.**

## Jurisdiction identity

Canonical public label: **Republic of Ireland**

Short display label may be **Ireland** only where the context cannot be confused with the island as a whole.

Do not use `Ireland` as a discovery scope when it could silently include Northern Ireland.

Public-service authority:

- Health Service Executive (HSE), Republic of Ireland.

Current operational geography:

- HSE Dublin and North East;
- HSE Dublin and Midlands;
- HSE Dublin and South East;
- HSE Mid West;
- HSE South West;
- HSE West and North West.

The HSE remains one national organisation, but each health region has its own budget, leadership and local decision-making responsibilities. Region- or service-specific access must therefore remain explicitly local.

## Readiness matrix

| Journey | Readiness | Current authoritative basis | Implementation rule |
| --- | --- | --- | --- |
| Adult autism assessment | **READY — bounded private-access route** | HSE public guidance states the HSE does not provide adult autism assessments and adults must currently use private assessment; HSE assessment-process guidance describes what adult assessment may involve. | Explain current access fact without recommending a provider. Preserve the difference between public-service absence and clinical standards. |
| Child autism assessment | **READY — national framework with local service routing** | HSE autism assessment guidance; HSE National Protocol for Autism Assessment and Intervention Pathways effective 25/03/2026; Children's Disability Network Team / primary-care referral guidance. | National protocol may describe assessment standards; actual service/referral destination can still depend on need and local service organisation. |
| Adult ADHD assessment | **READY — national model with regional implementation variation** | HSE ADHD in Adults Model of Care, updated June 2026; HSE parliamentary-response evidence about incomplete rollout and area-specific access. | Never convert the national model into a claim that a public Adult ADHD team is currently available everywhere. Current availability must be checked regionally. |
| Child ADHD assessment | **PARTIAL — not yet suitable for a strong national access promise** | HSE CAMHS operational guidance and implementation-plan material show a paediatric ADHD model/process is still being developed/rolled out. | Do not manufacture a uniform national pathway. Use only carefully bounded current local/service evidence until the national model is sufficiently settled. |
| Assessment of Need vs diagnosis | **READY — important cross-cutting distinction** | HSE Assessment of Need guidance under the Disability Act 2005. | AON is a legal needs/service process, distinct from autism/ADHD diagnostic assessment; an AON is not required to access HSE services. |
| Support while waiting / without diagnosis | **READY — bounded** | HSE autism and children's-disability guidance explicitly notes support/services may be available without a formal autism diagnosis or AON. | Link needs-led support without implying universal entitlement to a specific service. |

## Critical source set

### HSE autism access

Source:
`https://www2.hse.ie/conditions/autism/assessment-and-support/assessment-autism/`

Current bounded findings:

- a person may begin by speaking with a GP, public health nurse, other health professional, local CDNT/primary-care team or school staff as appropriate;
- children may be referred to community-based services and parents/guardians can self-refer to children's services;
- HSE public guidance currently states that the HSE does not provide autism assessments for adults;
- adults seeking autism assessment are directed to private assessment;
- support may be available while waiting and HSE services are not universally conditional on an autism diagnosis.

### HSE national autism protocol

Source:
`https://www2.healthservice.hse.ie/organisation/national-pppgs/hse-national-protocol-for-autism-assessment-and-intervention-pathways/`

Effective:
25 March 2026.

Current bounded finding:

The HSE has a national protocol intended to standardise clinical autism assessment and intervention pathways across HSE, HSE-funded and relevant private services. The protocol describes assessment approach; it must not be misrepresented as proof that the HSE currently provides adult public autism assessment everywhere.

### HSE adult ADHD model

Source:
`https://about.hse.ie/publications/hcp-adhd-in-adults-model-of-care/`

Published:
January 2021.

Updated:
June 2026.

Current bounded finding:

The model covers adult ADHD assessment, diagnosis, treatment and service configuration. Its existence does not prove uniform current service availability.

### Adult ADHD implementation variation

Sources include current HSE parliamentary-response pages such as:

- `https://about.hse.ie/publications/question-from-deputy-jennifer-whitmore-pq-3414-26/`
- `https://about.hse.ie/publications/question-from-deputy-cathy-bennett-pq-24040-26/`

Current bounded finding:

Adult ADHD services are implemented through area/catchment-specific teams and availability/capacity can vary. Any current-access Resource must name the region/service scope and review date.

### Children's disability services

Source:
`https://www2.hse.ie/babies-children/disabilities/services/getting-a-referral/`

Current bounded findings:

- parent/guardian self-referral is possible;
- professional referral is also possible;
- a child does not need a diagnosis or Assessment of Need to be referred to children's disability services;
- the appropriate destination may be primary care or a Children's Disability Network Team depending on need;
- waits vary locally.

### Assessment of Need

Source:
`https://www.hse.ie/services/disability/applying-for-an-assessment-of-need/assessment-of-need/`

Current bounded findings:

- Assessment of Need is a separate legal process under the Disability Act 2005;
- it identifies disability-related health/service needs;
- it is not required to access HSE health services;
- it must not be described as equivalent to autism or ADHD diagnostic assessment.

### HSE Health Regions

Source:
`https://about.hse.ie/leadership-and-operations/hse-health-regions/`

Current bounded findings:

- the HSE has six health regions;
- the HSE remains a single national organisation;
- regions have their own budgets, leadership and local decision-making responsibilities;
- smaller Health Areas sit beneath the regions.

## First implementation recommendation

Build **Ireland Assessment & diagnosis reference slice v1** with these initial governed journeys only:

1. **Adult autism assessment in the Republic of Ireland**
   - current public/private distinction;
   - what assessment may involve;
   - no provider recommendation;
   - support route separated from diagnosis.

2. **Child autism assessment in the Republic of Ireland**
   - national autism protocol;
   - parent/professional referral routes;
   - primary-care/CDNT distinction;
   - support not conditioned on diagnosis where the HSE source says so.

3. **Adult ADHD assessment in the Republic of Ireland**
   - national model;
   - GP/local adult mental-health referral structure where currently supported;
   - explicit regional-service availability caveat;
   - diagnosis kept separate from medication/treatment decisions.

4. **Assessment of Need versus diagnostic assessment in the Republic of Ireland**
   - legal needs assessment separated from clinical diagnosis;
   - no implication that AON is required for HSE service access.

Do **not** force a national child-ADHD access Question into v1 unless current first-party evidence can support it without pretending the evolving model is fully implemented.

## Proposed package hierarchy

`Republic of Ireland -> HSE Health Region -> Health Area / local service where material -> governed route`

Not every route needs all levels. A national HSE rule may remain national. A current service-availability statement should narrow to the appropriate region/service.

## Mandatory hostile boundaries

The first Ireland package must prove all of the following:

1. England Right to Choose never appears as an Irish entitlement.
2. Northern Ireland HSC Trust routes never appear as Republic-of-Ireland HSE routes.
3. Republic-of-Ireland HSE routes never appear as Northern Ireland NHS/HSC rules.
4. HSE Assessment of Need is not presented as a clinical autism/ADHD diagnosis.
5. Adult autism private-access facts do not become private-provider endorsement.
6. The national Adult ADHD Model of Care does not become a false claim of universal current public-team availability.
7. A local HSE service example never becomes a national Ireland rule.
8. Child-support routes do not become falsely diagnosis-dependent when authoritative HSE sources state otherwise.
9. Medication/prescribing remains outside diagnostic-route authority.

## Language

Primary authoritative sources in this readiness slice are available in English.

Irish-language public material may be added where useful, but English availability does not create a rule that future Ireland evidence must be English-only.

If Irish-language wording is later authoritative for a material legal/service distinction, preserve the original-language source and translation uncertainty according to the international architecture contract.

## Maintenance risks

### High-change areas

- Adult ADHD team rollout and catchment coverage.
- Child ADHD model-of-care development and implementation.
- Local wait/capacity information.
- Regional/Health Area service configuration during HSE restructuring.

### Lower-change anchors

- National HSE organisation identity.
- Distinction between HSE and Northern Ireland HSC/NHS.
- Assessment of Need being a distinct legal process.
- Core clinical boundary separating diagnosis from medication decisions.

High-change sources should use shorter review windows than stable architecture documents.

## Readiness verdict

**PASS — suitable first international pilot.**

The Republic of Ireland is ready for one bounded Assessment & diagnosis package.

It is **not** ready for a claim of comprehensive national neurodivergence coverage, and child ADHD should remain partial until current national access evidence is strong enough.

## Next implementation gate

The next routine task is to build the bounded Ireland Assessment & diagnosis candidate on a new branch.

That candidate must contain governed content, source matrix, additive discovery scope and hostile benchmarks, and therefore must pass the full exact-head content acceptance process before protected merge.
