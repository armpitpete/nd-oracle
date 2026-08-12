# The Neurodiverse Oracle — Production State v0.2

Status: accepted production evidence

Recorded: 2026-08-12

## Purpose

This document records the accepted production identity of whole-site v0.2 after the guarded repeat-production deployment completed successfully.

It is evidence of an already completed deployment. It does not itself deploy, publish, change DNS, alter Cloudflare configuration, or authorise a later production release.

Repository state, deployment artifact identity, Cloudflare deployment identity, and observed live state remain separate evidence and must not be silently conflated.

## Accepted repository and release identity

- Repository: `armpitpete/nd-oracle`
- Protected branch: `main`
- Accepted repository commit: `8339a64e7395a01ac1e53fa6ef2bca8ccb0899b5`
- Deployed exact commit: `8339a64e7395a01ac1e53fa6ef2bca8ccb0899b5`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful workflow run number: `4`
- Successful workflow run ID: `31577100075`
- Deployment artifact SHA-256: `4118b6df9930568290e2a2fe4543168963b7a7d2dcfe066aa3e69f58222f3543`
- Cloudflare Pages deployment identity: `a7a85a20.nd-oracle.pages.dev`
- Canonical production domain: `https://ndoracle.org`

At the time this state was recorded, protected `main` and the deployed release were the same exact commit. Future repository changes do not become production merely by existing on `main`; deployment remains a separate protected action.

## Deployment evidence

The successful production workflow re-resolved current `main`, checked out the exact release SHA, and completed the full release path before upload.

The accepted run recorded:

- exact checkout identity `8339a64e7395a01ac1e53fa6ef2bca8ccb0899b5`;
- knowledge validation PASS for all five authoritative objects and their governed evidence, uncertainty, perspective, reference, and graph routes;
- complete regression suite PASS: `229` tests;
- real whole-site v0.2 static build PASS;
- static deployment-boundary checks PASS;
- pinned Wrangler `4.114.0` verification PASS;
- Cloudflare Pages project identity `nd-oracle` PASS;
- Direct Upload configuration with production branch `main` PASS;
- dedicated project subdomain `nd-oracle.pages.dev` PASS;
- custom-domain set, after normalising the provider-owned Pages subdomain, exactly `ndoracle.org` PASS;
- artifact digest recorded before upload;
- `21` files uploaded successfully;
- `_headers` uploaded;
- Cloudflare reported deployment complete.

No custom-domain, DNS, redirect, zone, Pages project identity, or production-branch mutation was requested by the deployment workflow.

## Observed production presentation

A post-deployment owner-supplied screenshot visually confirmed the v0.2 homepage presentation in production context. The observed page contained the expected v0.2 public reading journey, including:

- the heading `Understand neurodivergence without doing all the digging yourself`;
- primary navigation `Understand`, `How it works`, and `About`;
- ordinary-language question entry points;
- the five current topics: ADHD, Autism, Executive function, Neurodiversity, and Sensory processing;
- the `Choose how deep to go` evidence/reasoning explanation;
- Accessibility and Privacy links;
- no visible unfinished feature catalogue on the homepage.

This screenshot is visual confirmation of the homepage presentation, not an independent network capture by the repository or CI system.

## Verification boundary

The deployment itself is proven complete by the successful guarded workflow and Cloudflare deployment output.

The assistant environment used during release verification could not independently resolve `ndoracle.org` after deployment. Therefore this record does **not** claim an independent post-release HTTP sweep of every canonical route, header, redirect, sitemap, robots response, or 404 response.

Those checks remain the next bounded production-quality verification lane. Their absence does not change the fact that the accepted v0.2 artifact was successfully deployed through the protected production path.

## Production content state

Whole-site v0.2 provides the public corpus through the reading-first site structure:

- `/`
- `/understand/`
- `/understand/neurodiversity/`
- `/understand/autism/`
- `/understand/adhd/`
- `/understand/executive-function/`
- `/understand/sensory-processing/`
- `/how-it-works/`
- `/about/`
- `/accessibility/`
- `/privacy/`

The legacy compatibility routes for tools, games, resources, community, and oracle remain intentionally outside the primary navigation and public sitemap and are expected to remain non-indexed unless a later accepted release changes that contract.

## Accepted publication conclusion

Whole-site v0.2 is accepted as deployed production state at the exact release identity above.

This acceptance means the public website milestone is complete. It does not mean the knowledge corpus is complete, nor does it waive later evidence, accessibility, route, security, or content review requirements.

## Still separate and protected

This accepted production state does not authorise any later:

- deployment or production replacement;
- DNS, redirect, hostname, or Cloudflare project mutation;
- schema version or migration;
- Oracle chatbot or AI answer interface;
- search or graph interface;
- accounts or profiles;
- forms, comments, direct messages, or community moderation infrastructure;
- analytics or advertising;
- collection of personal or sensitive data.

Any such change must pass the applicable governance and protected-change gates.

## Reopening condition

Before any later production claim, re-resolve protected `main`, candidate release identity, artifact identity, deployment result, and actual production state. Never infer deployment merely from a repository merge.
