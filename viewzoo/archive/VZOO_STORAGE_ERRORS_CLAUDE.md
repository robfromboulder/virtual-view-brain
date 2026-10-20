# Storage Errors: Claude Runbook

> Skip and log any view file or row that can't be read or parsed instead of failing catalog load, and keep the cause on every wrapped storage exception.
>
> **Branch:** `storage-errors` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — Storage error tests ← NEW in this branch

```bash
mvn test -Dtest=TestViewZooLocalFileSystemClient
mvn clean package -DskipTests && mvn test -Pintegration -Dtest='TestViewZooJdbcClient,TestViewZooIntegration'
```

**Expected:** all pass. Before the fix, on a macOS host, 10 unit and 17 integration tests fail. The integration run takes about 3½ minutes, longer before the fix because each crashing case waits 30 s and recreates the Trino container. `testCaseInsensitiveCollisionRejected` skips itself on a case-sensitive filesystem, and `testFileNameCollision` checks the rename message only on `testfsmount` under a macOS host.
