# International source-readiness probe — Australia v1

Date: 2026-09-05
Status: readiness pass
Parent architecture: `docs/INTERNATIONAL_EXPANSION_ARCHITECTURE_v1.md`

## Decision

**PASS — Australia supports a bounded Assessment & diagnosis package.**

The useful initial journeys are national autism-assessment orientation and national ADHD-assessment orientation. The package must make state/territory implementation visible rather than claiming one uniform public-service pathway.

## Why Australia is architecturally useful

Australia differs from the Republic of Ireland because national health orientation coexists with state/territory rules and service arrangements. Healthdirect explicitly notes state/territory differences in ADHD medicine prescribing. This makes Australia a useful test that a national Question can orient a reader without silently turning subnational rules into national rules.

## Source readiness

### Autism

Healthdirect Australia provides national public health information covering:
- speaking with a doctor/health professional when assessment is a concern;
- referral to specialist assessment for children;
- specialist diagnosis for adults;
- support/service orientation.

Source: `https://www.healthdirect.gov.au/autism`

Boundary: this does not establish one uniform public autism-assessment service in every state or territory.

### ADHD

Healthdirect Australia provides national public health information about ADHD, diagnosis and clinical roles and notes that state/territory rules differ for ADHD medicine prescribing.

Source: `https://www.healthdirect.gov.au/attention-deficit-disorder-add-or-adhd`

Related prescribing-boundary source:
`https://www.healthdirect.gov.au/adhd-medicine`

Boundary: diagnosis and medication authority remain separate; ND Oracle does not choose medicine, dose or prescriber.

## Language

The reviewed sources used for this bounded package are English-language first-party Australian public-health pages. No translation is required for the candidate. This does not create an English-only rule for future Australian evidence.

## Freshness ownership

Critical sources:
- Healthdirect autism;
- Healthdirect ADHD;
- any future state/territory service route added to this package.

National information uses the normal authoritative-guidance review cadence. State/territory service or prescribing implementation should use a shorter cadence when it is volatile.

## Readiness verdict

Australia meets the no-empty-country rule:
- two real user journeys;
- current national public-health sources;
- explicit state/territory uncertainty;
- governed Questions/Resources;
- additive scope sidecar;
- deterministic and hostile benchmark.

No broader Australian corpus is authorised by this readiness pass.
