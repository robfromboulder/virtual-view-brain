# PG Refresh: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `pg-refresh` off `v483`
  * commit changes on branch
  * create draft PR against `v483`
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_PG_REFRESH_CLAUDE.md`
  * manual checks — capture steps in `VZOO_PG_REFRESH_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
* carry the fix forward to the next version branch when it is cut
* follow-on items from `viewzoo/archive/VIEWZOO_PG_NOTES.md`: small JDBC fixes, connection pool and configurable table, `jsonb` and metadata columns, history table
