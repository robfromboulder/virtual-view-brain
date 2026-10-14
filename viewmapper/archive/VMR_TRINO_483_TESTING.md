# Trino 483: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout each check folds into the project repo `CLAUDE.md` of the lobe it exercises.

## Setup

`./build.sh` has produced `viewmapper:483`. `ANTHROPIC_API_KEY_FOR_VIEWMAPPER` holds a real key and `ANTHROPIC_MODEL` is unset, so the default model runs. A model that skips tools still writes plausible prose, so each check looks for numbers only a tool can produce.

## Test cases

1. **CLI tool loop on Sonnet 5.5** — from `viewmapper-agent/`, run `java -jar target/viewmapper-483.jar run --connection "test://<dataset>" "Analyze this schema and suggest where to start"` for each of `simple_ecommerce`, `moderate_analytics`, `complex_enterprise` and `realistic_bi_warehouse`.
   - **Expected:** each answer names the complexity level and view count and lists dependent counts or centrality scores. Passed 2026-10-12 on all four, about 10 s each.
2. **CLI diagram** — run `java -jar target/viewmapper-483.jar run --connection "test://complex_enterprise" "Show me a mermaid diagram of the views around customer_360"`.
   - **Expected:** a Mermaid block of the subgraph around `customer_360`, not the whole schema, with `customer_360` styled as the focus. Passed 2026-10-12 in about 11 s.
3. **Claude Desktop, test dataset** — configure Claude Desktop with the `viewmapper:483` image and `VIEWMAPPER_CONNECTION=test://complex_enterprise`, then ask "what are the central hub views?".
   - **Expected:** the tool-call panel shows ViewMapper's tool being called, and the answer lists hubs with centrality scores.
4. **Claude Desktop, JDBC** — configure a `jdbc:trino://` connection to a live server, ideally one older than 483, and ask what catalogs are available, then analyze a schema with views.
   - **Expected:** catalogs and schemas list, and the analysis reports that schema's views; the 483 driver connects without errors.
