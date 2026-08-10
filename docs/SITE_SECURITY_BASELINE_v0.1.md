# The Neurodiverse Oracle — Site Security Baseline v0.1

Status: implementation candidate

This baseline keeps Site Shell v0.1 intentionally low-risk: static files, no server-side runtime, no accounts, no forms, no analytics scripts and no personal-data collection.

## 1. GitHub repository baseline

### Implemented in the candidate

- `main` remains the protected release authority.
- validation runs on pull requests to `main`.
- workflow `GITHUB_TOKEN` permission is explicitly read-only for repository contents.
- external GitHub Actions are pinned to full commit SHAs.
- checkout credentials are not persisted after checkout.
- Python sources are compiled before validation/tests.
- Dependabot checks GitHub Actions and Python dependencies monthly.
- generated deployment output remains uncommitted.

### Repository settings to verify before public launch

- direct force pushes to `main`: disabled;
- deletion of `main`: disabled;
- required `validate` status check: enabled;
- pull requests required for `main` changes where the account/repository configuration supports the intended workflow;
- conversation resolution required before merge when review comments exist;
- administrator bypass kept as narrow as practical;
- GitHub Actions allowed-actions policy restricted to the actions actually required;
- require full-length SHA pinning for Actions if the repository plan exposes that policy;
- private vulnerability reporting enabled before inviting public security reports;
- secret scanning and push protection enabled where available.

Do not require an approval configuration that makes the owner unable to merge because no independent eligible reviewer exists. Exact-head owner acceptance plus mandatory validation remains preferable to a cosmetic review rule that cannot be satisfied.

## 2. Static application baseline

Global defaults:

- no JavaScript;
- no forms;
- no inline styles;
- no external fonts;
- no third-party embeds;
- no analytics beacon;
- no advertising tracker;
- no client storage requirement;
- no Pages Functions / Workers runtime for the shell.

The Content Security Policy defaults to `default-src 'none'` and selectively permits only same-origin styles, fonts and media plus same-origin/data images. Scripts, network connections, objects, forms and framing remain blocked globally.

Future interactive features must use the smallest route-specific relaxation possible. Do not weaken the global policy merely because one game or tool needs JavaScript.

## 3. Cloudflare Pages baseline

### Deployment model

Use a built `dist/` artifact produced from an exact accepted `main` SHA. Direct Upload is preferred while deployment remains an explicit protected action because a repository merge must not silently become a production deployment.

### Static response controls

The deployment includes a Cloudflare Pages `_headers` file with:

- restrictive Content Security Policy;
- HSTS;
- frame blocking;
- MIME-sniffing protection;
- no-referrer policy;
- restrictive Permissions Policy;
- same-origin opener/resource policy;
- legacy cross-domain policy disabled.

### Zone settings to verify when the custom domain is activated

- SSL/TLS encryption mode: **Full (strict)** where applicable;
- **Always Use HTTPS**: on once the entire zone is HTTPS-ready;
- **Automatic HTTPS Rewrites**: optional safety net, not a substitute for writing HTTPS/relative asset URLs correctly;
- DNSSEC: enable after the Cloudflare nameserver migration is stable and the correct DS record can be published at the registrar;
- WAF: retain the Free Managed Ruleset/default managed protection available to the plan;
- do not enable broad challenge/bot settings merely for appearance of security — the static shell has little application attack surface and unnecessary challenges create user burden;
- no Web Analytics or other injected client script until a separate privacy decision authorises it.

## 4. Domain and account controls

Before public launch verify:

- strong unique passwords for GitHub, Cloudflare and registrar accounts;
- multi-factor authentication on all three;
- recovery codes stored offline;
- registrar transfer/domain lock enabled;
- registrar contact/recovery email is controlled and secured;
- Cloudflare API tokens, if later created, are least-privilege and never committed to the repository.

## 5. Personal data boundary

Site Shell v0.1 collects no personal data by design.

Any future feature involving accounts, submitted stories, contact forms, saved preferences, Oracle queries, health information or community moderation is a new security/privacy boundary and requires before implementation:

1. threat model;
2. data-flow inventory;
3. lawful/privacy basis review;
4. retention/deletion policy;
5. abuse and safeguarding analysis;
6. authentication/authorisation design where relevant;
7. explicit owner approval.

## 6. Release proof

A production release is not proven by a successful repository build alone.

Before accepting a release, preserve separate evidence for:

1. exact repository commit;
2. passing validation/tests;
3. deterministic site build;
4. deployment identity;
5. custom-domain identity;
6. live HTTPS response;
7. live security headers;
8. navigation/function checks against the real public site.

Do not substitute a preview, local build, Pages project, DNS record or successful deployment command for verification of the actual public site.
