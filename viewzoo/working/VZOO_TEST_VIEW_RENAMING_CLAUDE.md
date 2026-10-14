# Test View Renaming: Claude Runbook

> Implement `ALTER VIEW ... RENAME TO` in ViewZoo and cover it with integration tests.
>
> **Branch:** `test-view-renaming` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — Rename integration test ← NEW in this branch

```bash
mvn clean package && mvn test -Pintegration
```

**Expected:** the package step runs 14 unit tests, including `TestViewZooMetadata` and `TestViewZooLocalFileSystemClient`, with 0 failures. The integration step takes ~30s with Docker running; 8 tests pass, 0 failures — four tests (including `testViewRenaming`) on each of `testjdbc` and `testfs`.