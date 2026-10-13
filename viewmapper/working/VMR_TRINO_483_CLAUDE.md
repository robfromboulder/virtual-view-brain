# Trino 483: Claude Runbook

> Move ViewMapper to version branches, freezing `v479`, and upgrade to Trino 483 on a new `v483` branch via a reviewed PR, with Sonnet 5.5 replacing the retired default model, released as `483a`.
>
> **Branch:** `trino-483` · **Blocked-by:** —

## Running Tests

Run the steps from the platform runbook first (if the brain has one), verifying results match the expectations documented there. Then run the work-specific step(s) below.

### Step 1 — agent and MCP server suites

```bash
cd viewmapper-agent && mvn clean package
cd ../viewmapper-mcp-server && ./venv/bin/pytest -q
```

**Expected:** 215 agent tests pass in under a minute, including `TrinoSqlParserTableFunctionTests` (8) and the two `PIVOT` cases in `TrinoSqlParserEdgeTests`; 14 MCP server tests pass. Six of the eight table-function tests fail if `DependencyExtractor::visitTableArgument` is removed.

### Step 2 — image

```bash
./build.sh
```

**Expected:** `viewmapper-483 is go 🚀` and a local image `viewmapper:483`.
