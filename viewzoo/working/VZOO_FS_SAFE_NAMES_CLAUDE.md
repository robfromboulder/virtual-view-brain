# FS Safe Names: Claude Runbook

> Filesystem storage rejects view names it can't store as one flat file on Linux or macOS, leaving JDBC storage unchanged.
>
> **Branch:** `fs-safe-names` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step N — filesystem name tests ← NEW in this branch

```bash
mvn test -Dtest=TestViewZooLocalFileSystemClient
mvn clean package -DskipTests && mvn test -Pintegration
```

**Expected:** all unit and integration tests pass. The integration output reports `testfs` as case-sensitive and, on a macOS host, `testfsmount` as case-insensitive.
