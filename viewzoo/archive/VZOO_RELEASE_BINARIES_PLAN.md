# Release Binaries: Implementation Plan

## Objective

Publish a prebuilt ViewZoo plugin for each Trino version as a GitHub release, built and tested on the maintainer's Mac by following a procedure in the repository's `CLAUDE.md`, so users can install without Java or Maven. Release tags are always the Trino version plus a letter, starting at `a`, and never the bare version. Targets the `v483` branch, giving the first published release, `483a`. No workflow, no release script, no code changes.

## Context

See `VZOO_RELEASE_BINARIES_FINDINGS.md` in this directory for the decision record and alternatives considered.

Key references in the owning lobe:
- `VZOO_SCOPE.md` — problem space this fits into
- `VZOO_FINDINGS.md` — relevant prior decisions
- `VZOO_APPROACH.md` — design constraints

## What changes

- `pom.xml` — give `io.airlift:configuration-testing` test scope, so the test library stops shipping in the plugin directory and release zip.
- `CLAUDE.md` — a "Releasing" section, run when Rob asks for a release:
  1. Check that the working tree is clean, the version branch matches its remote, and the tag doesn't exist yet.
  2. `mvn clean package`, then `mvn test -Pintegration`.
  3. Copy `target/viewzoo-<version>.zip` to `viewzoo-<tag>.zip` and compute its SHA-256 with `shasum -a 256`.
  4. Unpack the zip into a clean `trinodb/trino:<version>` container with a filesystem catalog, and create and query a view.
  5. `gh release create <tag> --draft --target <commit>` with the zip attached and the checksum in the notes.
  6. After Rob reviews the draft, publish it, which creates the tag.
- `README.md` — make downloading a release the first install path, with build-from-source as the alternative.

## Interaction with existing code

| Existing code | Interaction | Risk |
|---|---|---|
| The trino-maven-plugin's `target/viewzoo-<version>.zip` | Becomes the release artifact | If the plugin stops producing it, the procedure must zip `target/viewzoo-<version>` itself |
| Tags `467` and `470` | Bare-version tags with no release | They predate the naming rule and stay as plain tags; any release of those versions would be `467a` or `470a` |
| GitHub default branch | Stays `v479` until `483a` is published, then switches to `v483` | `v479` is never changed, so it gets no release |

## Testing approach

The full unit and integration suites must stay green after the scope change, and the plugin directory must no longer contain `configuration-testing`. The release procedure carries its own checks: the integration run, the clean-container install, and the draft reviewed before it is published.

## Implementation sequence

1. Scope fix in the pom, with a full test run.
2. The "Releasing" section in `CLAUDE.md`.
3. README install path.
4. Merge, run the procedure for `483a`, publish, and switch the default branch.

## Scope boundary — what this does NOT include

- A GitHub Actions workflow or a committed release script.
- Maven Central publishing, container images, or artifact signing.
- Releases for branches older than `v483`.
- Any change to the build beyond the dependency scope.

## Resolved questions

1. Older versions get no releases (Rob).
2. Only the plugin zip is attached. The release's tag marks the built commit, and GitHub attaches source archives of the tag to every release (Rob).
