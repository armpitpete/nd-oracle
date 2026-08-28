# Ecosystem v0.6 release boundary

A branch, pull request or passing test suite is not a production release.

Release identity exists only after:

1. protected schema/publication acceptance;
2. merge at an exact accepted head;
3. re-resolution of protected `main`;
4. explicit production deployment authorisation;
5. guarded deployment from exact `main`;
6. independent live verification;
7. a production-state record freezing commit and artifact identity.

Until then, all v0.6 language must say candidate rather than live or deployed.
