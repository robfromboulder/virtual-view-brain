# Why ViewZoo: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `why-viewzoo` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review doc changes
  * full rebuild and automated retest on PR code
  * review PR description against final docs one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_WHY_VIEWZOO_CLAUDE.md`
  * manual checks — capture steps in `VZOO_WHY_VIEWZOO_TESTING.md`
  * comparison-table claims checked 2026-10-20 against Trino 483 docs (memory, Hive, metastores), Hive admin manual, Spark Hive docs, Iceberg REST spec, Iceberg `JdbcUtil.java`, Polaris and Lakekeeper docs — all hold; closes plan open issue 3
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * deviation: "Why ViewZoo?" is the README's last section, not near the top as the plan says (Rob's call)
  * deviation: the two-workflow framing (git for filesystem, shared data for JDBC) lives in the tradeoffs column of the "Why ViewZoo?" table, which replaces the plan's comparison columns, and the storage-section intros only say how each mode stores views
