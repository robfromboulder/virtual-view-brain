# Trino 479 Update: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout these fold into the canonical testing doc.

## Setup

Trino 479 instance running locally or accessible for JDBC connection. JDK 25 installed.

## Test cases

1. **Agent CLI against Trino 479** — run the agent CLI against a Trino 479 catalog and verify schema exploration and lineage output.
   - **Expected:** Output matches pre-upgrade baseline; no errors or missing data
2. **MCP server startup** — start the MCP server subprocess and confirm it initializes without errors.
   - **Expected:** Clean startup, responds to requests