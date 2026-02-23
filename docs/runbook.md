# Runbook

## Purpose
How to run agent workflows safely and roll back.

## Run
1. Decide the desired state and checkpoint.
2. Run the workflow:
   - GitHub Actions: verify secrets are set
   - Local: validate env vars
3. Verify outputs match acceptance criteria.

## Rollback
1. Identify the last known-good commit.
2. Revert if necessary.
3. Re-run CI and sanity checks.

## Notes
- Keep economic metrics in the agent README.
- Treat tools and secrets as explicit dependencies.
