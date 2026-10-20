# Storage Errors: Burndown

Everything between working code and a merged PR.

* PR wrangling
  * create branch `storage-errors` off `v483`
  * commit changes on branch
  * create draft PR
  * review code changes
  * full rebuild and automated retest on PR code
  * review PR description against final code one last time
  * request feedback from reviewers
  * respond to review feedback
* testing
  * automated checks — see `VZOO_STORAGE_ERRORS_CLAUDE.md`
  * manual checks — capture steps in `VZOO_STORAGE_ERRORS_TESTING.md`
* docs
  * take screenshots
* mini-brain closeout — note deviations and reversals here; `VV_WORK_CLOSEOUT.md` consumes them
  * deviation: the corrupt-file integration case is its own test, `testUnreadableFileSkipped`, not an extension of `testUnsupportedFileNamesSkipped`, because a bad entry stops the Trino server and would mask that test's assertions; the tests recover by deleting mounted files from the host and recreating the container (`recoverTrino`)
  * deviation: `renameView` runs the case-collision check before the link, as `createView` does, not in the `FileAlreadyExistsException` handler, because `isExactFile` throws `IOException`, which a sibling catch clause can't handle
  * deviation: an end-to-end JDBC test, `testUnloadableRowsSkipped`, was added beyond the plan so the JDBC warning text is checked
  * reversal: see the Reversals section of `VZOO_STORAGE_ERRORS_FINDINGS.md`
* carry the change forward when the next version branch is cut
