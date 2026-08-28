# Ecosystem v0.6 stop rule

Routine reversible implementation and repair continue automatically.

Stop only when one of these is reached:

- the exact candidate fails in a way that requires a protected product/governance decision rather than a technical repair;
- protected schema/publication acceptance is required;
- merge to protected main is required;
- production deployment is required;
- a secret/credential, destructive action or physical owner action is required.

CI failures, test repairs, documentation corrections and reversible branch work are not stop conditions.
