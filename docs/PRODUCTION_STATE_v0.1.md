# The Neurodiverse Oracle — Production State v0.1

Status: accepted production evidence

Recorded: 2026-08-10

## Purpose

This document records the accepted production identity of Site Shell v0.1. It is evidence of an already completed deployment and DNS/domain activation. It does not itself deploy, publish, redirect, configure DNS, or authorise later production changes.

Repository state and production state remain separate identities and must not be silently conflated.

## Accepted repository and release identity

- Repository: `armpitpete/nd-oracle`
- Protected branch: `main`
- Accepted repository commit: `5fa502bf717adb0e4c900eda7594bcbc4f74a6f0`
- Deployed exact commit: `5fa502bf717adb0e4c900eda7594bcbc4f74a6f0`
- Deployment artifact SHA-256: `cf8df0c9b87448fb75bcbdccf3d1cead276bbcbb67fb65f4808ed397d0d5323c`
- Canonical production domain: `https://ndoracle.org`

At the time this state was accepted, repository `main` and the deployed release pointed to the same exact commit. Future repository changes do not become production merely by existing on `main`; deployment remains a separate protected action.

## Accepted live route verification

The following canonical routes were verified live with HTTP 200:

- `/`
- `/understand/`
- `/tools/`
- `/games/`
- `/resources/`
- `/community/`
- `/oracle/`
- `/about/`
- `/accessibility/`
- `/privacy/`

This evidence records the verification performed for the accepted release. It is not a claim that future production will remain unchanged without re-verification.

## Accepted production security baseline

The accepted live release was verified with:

- strict Content-Security-Policy;
- HTTP Strict Transport Security;
- `X-Frame-Options: DENY`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- restrictive Permissions-Policy;
- `Cross-Origin-Opener-Policy: same-origin`;
- `Cross-Origin-Resource-Policy: same-origin`.

The repository regression tests remain the pre-deployment contract; live verification remains separate evidence after deployment.

## DNS and hostname state

Accepted hostname state:

- apex `ndoracle.org` resolves through a proxied Cloudflare apex CNAME to `nd-oracle.pages.dev`;
- existing Google mail configuration was preserved;
- Google MX remains directed to `smtp.google.com`;
- Google DKIM remains present;
- SPF remains `v=spf1 include:_spf.google.com ~all`;
- Google site-verification remains present;
- `www.ndoracle.org` has the documented proxied placeholder DNS record;
- an active Cloudflare Single Redirect sends HTTP or HTTPS `www` requests to HTTPS apex with path and query-string preservation.

Verified redirect example:

`http://www.ndoracle.org/understand/?q=test`

→ `https://ndoracle.org/understand/?q=test`

## Still separate and protected

This accepted production state does not authorise any later:

- deployment or production replacement;
- DNS or redirect change;
- schema version or migration;
- Oracle chatbot or AI answer interface;
- search or graph interface;
- accounts or profiles;
- forms, comments, direct messages, or community moderation infrastructure;
- analytics or advertising;
- collection of personal or sensitive data.

Any such change must pass the applicable governance and protected-change gates.

## Reopening condition

Re-resolve repository `main`, the candidate release identity, and the actual production state before any later deployment or production claim. Never infer deployment merely from a repository merge.