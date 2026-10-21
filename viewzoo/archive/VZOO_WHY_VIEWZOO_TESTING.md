# Why ViewZoo: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout each check folds into the project repo `CLAUDE.md` of the lobe it exercises.

## Setup

Build the plugin with `mvn clean package -DskipTests`. Add a temporary `src/test/docker/trino/catalog/pg.properties` with `connector.name=postgresql`, `connection-url=jdbc:postgresql://postgres:5432/postgres`, `connection-user=postgres` and `connection-password=secretpassword`. From `src/test/docker`, run `PROJECT_ROOT=<repo root> docker compose -p vzpgcheck up -d` and wait until `trino --execute 'SELECT 1'` succeeds in the Trino container. Afterwards run `docker compose -p vzpgcheck down -v` and delete `pg.properties`.

## Test cases

1. **PostgreSQL connector lists stored views** — create `testjdbc.example.hello` and `testjdbc.sales.orders_v`, then run the README's `select schema, view_name from pg.public.viewzoo order by schema, view_name`.
   - **Expected:** rows `example, hello` and `sales, orders_v`; `select *` also returns each view's JSON definition. Passed 2026-10-20.
2. **Row written outside the connector needs a restart** — in the Postgres container, `insert into viewzoo select 'example','copy',definition from viewzoo where view_name='hello'`, then `show tables from testjdbc.example`; restart the Trino container and repeat.
   - **Expected:** only `hello` before the restart; `copy` and `hello` after, and `select * from testjdbc.example.copy` returns `A, 1`. Passed 2026-10-20.
3. **README renders on GitHub** — open the README on the `why-viewzoo` branch, check that the comparison table renders and that every table-of-contents link resolves, `#why-viewzoo` included.
   - **Expected:** table and anchors render correctly. Not yet run.
