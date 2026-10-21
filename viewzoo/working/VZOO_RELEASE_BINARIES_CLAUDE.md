# Release Binaries: Claude Runbook

> Publish a prebuilt plugin for each Trino version as a GitHub release (`483a`, `483b`, …), built, tested and released from the maintainer's Mac by a procedure in the repository's `CLAUDE.md`.
>
> **Branch:** `release-binaries` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — Build without the test library ← NEW in this branch

```bash
mvn clean package && mvn test -Pintegration
ls target/viewzoo-483 | grep configuration-testing
```

**Expected:** all tests pass, and the `grep` prints nothing.
