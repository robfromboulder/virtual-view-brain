# Release Binaries: Decision Record

## Problem

The only way to install ViewZoo is to build it: clone the right version branch, install Java 25 and Maven, run `mvn clean package`, and copy `target/viewzoo-<version>` into Trino's plugin directory (issue #12). Someone who only wants to run Trino with ViewZoo has to set up a Java build toolchain first. The repository has version branches `v470` and `v475` through `v479`, and tags for two old Trino versions, `467` and `470`, but no GitHub release and no published binary for any version.

## Preferred approach: a GitHub Actions workflow that releases on a version tag

A workflow on each version branch builds the plugin and publishes it as a GitHub release whenever a release tag for that Trino version is pushed. The release carries one archive of the plugin directory, ready to unpack into `$TRINO_HOME/plugin/viewzoo`.

Every release tag is the Trino version plus a letter: `479a` is the first release for Trino 479, then `479b`, and so on. A bare version (`479` or `v479`) is never a release tag. Each release is uniquely named from the start, so no release is ever replaced and a tag always identifies exactly one binary.

| Aspect | Detail |
|---|---|
| Trigger | Pushing a tag matching `<version><letter>` that points at a commit on that version's branch; bare-version tags never trigger it |
| Build | `mvn clean package` with Java 25 on a GitHub-hosted runner, then the integration tests (`-Pintegration`) against the built plugin, since the runner has Docker; a failure publishes nothing |
| Artifact | `viewzoo-<tag>.zip` (e.g. `viewzoo-479a.zip`) of `target/viewzoo-<version>`, the directory the README already tells users to copy; the pom version stays the bare Trino version |
| Release | A GitHub release for the tag, with the archive attached and its SHA-256 checksum in the release notes |
| Per-branch | The workflow file lives on each version branch, because a tag's workflow runs from the tagged commit |

- **Matches the branch model** — one Trino version per branch, with the letter counting releases within it.
- **No replaced releases** — a fix is a new letter, so a downloaded `479a` never silently differs from another `479a`.
- **No new infrastructure** — GitHub Actions and Releases come with the repository.
- **Reproducible** — every published binary is built from a tagged commit by a recorded workflow run, not on someone's laptop.

## Alternatives considered

- **Publish to Maven Central** — the conventional home for Java artifacts, but Trino plugins are installed by copying a directory, not resolved by Maven, and Central publishing needs signing keys and an account. It adds work without making installation easier.
- **Tag releases with the bare Trino version** — matches the existing `467` and `470` tags, but a fix then either replaces the release's archive or needs a suffix added after the fact. Rejected so that every release is uniquely named from the start.
- **Build a release on every push to a version branch** — always current, but publishes unreviewed intermediate states and gives no release a stable name.
- **Upload binaries by hand** — no workflow to maintain, but not reproducible and easily forgotten.
- **Publish a Trino container image with ViewZoo installed** — convenient for Kubernetes users, but it is a second artifact to maintain. It could follow later.

## What this doesn't solve

- Users still need the binary built for exactly their Trino version; versions without a branch get nothing.
- Older branches get binaries only if the workflow is backported to them.
- Binaries are verifiable only by checksum; they carry no signature or build attestation.
