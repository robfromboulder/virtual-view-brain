# Release Binaries: Implementation Plan

## Objective

Publish a prebuilt ViewZoo plugin for each Trino version as a GitHub release, built by a GitHub Actions workflow when a version tag is pushed, so users can install without Java or Maven. Release tags are always the Trino version plus a letter, starting at `a`, and never the bare version. Targets the `v483` branch, giving the first published release, `483a`. No code changes.

## Context

See `VZOO_RELEASE_BINARIES_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `.github/workflows/release.yml` (new) — on a push of a tag matching `<version><letter>`: check that the tag's version matches the pom version, set up Java 25, run `mvn clean package`, then the integration tests with `mvn test -Pintegration` (they are excluded by default and need the built plugin), zip `target/viewzoo-<version>` as `viewzoo-<tag>.zip`, and create a GitHub release for the tag with the archive and its SHA-256 checksum. The job needs `contents: write` permission to create the release.
- `README.md` — make downloading a release the first install path, with build-from-source as the alternative. Add a short release procedure for maintainers, including the tag naming rule, or put it in `CONTRIBUTING.md`.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| `TestViewZooIntegration` | Runs in the workflow, starting Postgres and Trino with docker compose | Slow or flaky on hosted runners; may need longer timeouts |
| Tags `467` and `470` | Bare-version tags with no release, pointing at commits that don't contain the workflow | They predate the naming rule and stay as plain tags; any release of those versions would be `467a` or `470a` |
| GitHub default branch | Stays `v479` until `483a` is published, then switches to `v483` | `v479` is never changed, so it gets no release |
| `VZOO_WHY_VIEWZOO` and `VZOO_SECURITY_GUIDE` work items | All three edit the README | Whichever merges later rebases its README edit |

## Testing approach

The workflow is the test. Run it first in a throwaway private repository, such as `viewzoo-release-test`, holding a copy of the `release-binaries` branch, so no real release letter is spent or deleted in testing. GitHub doesn't allow forking a repository into the account that owns it. Then check by hand that the release appears, the archive unpacks to a working plugin directory, and Trino 483 starts with it. Those steps go in `VZOO_RELEASE_BINARIES_TESTING.md`.

## Implementation sequence

1. Write the workflow, push it to a throwaway private repository, and run it there.
2. Check the archive by installing it into a clean Trino 483.
3. Update the install docs.
4. Merge, tag `483a`, and confirm the published release.

## Scope boundary — what this does NOT include

- Maven Central publishing, container images, or artifact signing.
- Releases for branches older than `v483`.
- Any change to the build itself, beyond what packaging the archive needs.

## Open issues

1. Whether to release older versions. `v470` and `v475`–`v479` would each need the workflow backported and an `a` tag. `467` has no branch: its commit sits in the history of `main` and `v470`. A manually triggered run that builds a given commit would cover old versions without backporting.
2. Whether to attach the sources jar the build also produces, or only the plugin directory.
