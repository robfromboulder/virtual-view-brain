# FS Safe Names: Manual Test Plan

Checks run by hand for this work item (UI, API calls, data checks). At closeout each check folds into the project repo `CLAUDE.md` of the lobe it exercises.

## Setup

Trino 483 running natively on macOS, with `viewzoo.dir` on a case-insensitive APFS volume (the default). Install the plugin with `mvn clean package -DskipTests && cp -r ./target/viewzoo-483 $TRINO_HOME/plugin/viewzoo` and add a catalog `vzsmoke` with `connector.name=viewzoo`, `viewzoo.storage_type=filesystem` and `viewzoo.dir` set to an empty directory. Each view below is created with `AS SELECT 1 AS x`.

## Test cases

1. **Portable names** — create views `vzsmoke.s."a b\:*?<>|%"` and `vzsmoke.s."café😀"`.
   - **Expected:** both succeed and each writes one `s.<table>.json` file in `viewzoo.dir`.
2. **Case-fold collision** — create `vzsmoke.s."ß"`, then `vzsmoke.s."ss"`, then `CREATE OR REPLACE VIEW vzsmoke.s."ß"`.
   - **Expected:** `ss` fails with `ALREADY_EXISTS: View conflicts with an existing view file in filesystem storage`; replacing `ß` succeeds.
3. **Rejected names** — create views whose table is `"a/b"`, whose schema is `"/tmp"`, whose table is `cafe` followed by U+0301 (NFD), and whose table is 90 CJK characters (277-byte file name).
   - **Expected:** each fails with `INVALID_ARGUMENTS`, and no file is written inside or outside `viewzoo.dir`.
4. **255-byte boundary** — create a view whose table is `ab` followed by 82 CJK characters (exactly 255-byte file name).
   - **Expected:** succeeds.
5. **Failed rename** — `ALTER VIEW vzsmoke.s."ß" RENAME TO vzsmoke.s."x/y"`, then query `vzsmoke.s."ß"`.
   - **Expected:** the rename fails with `INVALID_ARGUMENTS`; the source still queries.
6. **Restart and skipped file** — copy any view file to `Upper.Case.json` in `viewzoo.dir` and restart Trino.
   - **Expected:** `server.log` warns `Skipping file whose name is not a view name Trino can create` naming `Upper.Case.json`; `SHOW TABLES FROM vzsmoke.s` lists exactly the views created above, and each still queries.

All six passed on 2026-10-19 against `156b6f2`.
