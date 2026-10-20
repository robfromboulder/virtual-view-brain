# Safe Create: Claude Runbook

> Make `createView` all-or-nothing in storage and refuse an existing view at the storage level unless `OR REPLACE` is given.
>
> **Branch:** `safe-create` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — Safe create tests ← NEW in this branch

```bash
mvn test -Dtest='TestViewZooLocalFileSystemClient,TestViewZooMetadata'
mvn clean package -DskipTests && mvn test -Pintegration -Dtest='TestViewZooJdbcClient,TestViewZooIntegration'
```

**Expected:** all pass. Before the fix, 2 unit and 4 integration tests fail. The integration run takes under 2 minutes. `testReplaceDoesNotWriteInPlace` skips itself when run as a user who ignores file permissions, such as root.
