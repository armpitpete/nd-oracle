# v0.7 deployment entrypoint repair

Deployment run #10 (`33172730697`) for exact main `b161bf73700d17fd9fb3be475ae910daaac0b4c5` stopped before Cloudflare upload.

The protected-main guard, checkout identity, compilation, 30-object validation and 291-test regression suite all passed. The failure occurred only when the workflow executed the production build command directly:

`python scripts/build_site.py`

The v0.7 wrapper imported `scripts.build_site_v06`, which works when the repository root is already on `sys.path` (as in the unit-test import path) but not when Python executes a file inside `scripts/` directly. The same latent issue existed in `scripts/verify_live_site.py`.

The repair explicitly adds the repository root to `sys.path` only for direct-script execution (`__package__` is empty), preserving normal package imports unchanged.

Regression coverage now executes the same direct builder command in an isolated temporary repository copy and directly invokes the live verifier with a deliberately non-HTTPS origin so its import/CLI path is tested without making a network request.

No Cloudflare deployment occurred in failed run #10, so the accepted v0.6 production site was not modified.
