# Release Binaries: Decision Record

## Problem

The only way to install ViewZoo is to build it: clone the right version branch, install Java 25 and Maven, run `mvn clean package`, and copy `target/viewzoo-<version>` into Trino's plugin directory (issue #12). Someone who only wants to run Trino with ViewZoo has to set up a Java build toolchain first. The repository has version branches `v470`, `v475` through `v479` and `v483`, and tags for two old Trino versions, `467` and `470`, but no GitHub release and no published binary for any version.

## Preferred approach: releases built and published from the maintainer's Mac

A "Releasing" section in the repository's `CLAUDE.md` holds the procedure, and Claude runs it on Rob's Mac when Rob asks for a release. The build already produces `target/viewzoo-<version>.zip`, holding the plugin directory under a top-level `viewzoo-<version>/` folder, ready to unpack into `$TRINO_HOME/plugin/`; the release attaches that zip.

Every release tag is the Trino version plus a letter: `483a` is the first release for Trino 483, then `483b`, and so on. A bare version (`483` or `v483`) is never a release tag. Each release is uniquely named from the start, so no release is ever replaced and a tag always identifies exactly one binary.

| Aspect | Detail |
|---|---|
| Source | A clean checkout of the version branch that matches its remote |
| Build | `mvn clean package`, then the integration tests (`-Pintegration`); a failure publishes nothing |
| Artifact | `target/viewzoo-<version>.zip` attached as `viewzoo-<tag>.zip` (e.g. `viewzoo-483a.zip`), about 15 MB; the pom version stays the bare Trino version |
| Check | The zip unpacked into a clean `trinodb/trino:<version>` container, and a view created through it |
| Release | A draft GitHub release created with `gh` at the tested commit, then published, which creates the tag |
| Procedure | The repository's `CLAUDE.md`; no workflow file and no release script |

- **No published build environment** — Rob doesn't want a copy of the build and test environment published as a GitHub Actions workflow, so nothing about it runs on or is described for GitHub.
- **Same artifact** — the plugin is pure Java with no native code and targets Java 25, which Trino 483 runs on, so a build on macOS matches one from a Linux runner.
- **Draft before publish** — a draft release has no tag until published, so a release can be checked without spending a letter.
- **Matches the branch model** — one Trino version per branch, with the letter counting releases within it.
- **No replaced releases** — a fix is a new letter, so a downloaded `483a` never silently differs from another `483a`.

## Alternatives considered

- **A GitHub Actions workflow that releases on a tag** — reproducible from a recorded run, but publishes the build and test environment as a workflow. Rejected by Rob.
- **A committed release script** — repeatable, but visible in the repository like a workflow, and the procedure is run by Claude, which follows written steps as reliably.
- **Publish to Maven Central** — the conventional home for Java artifacts, but Trino plugins are installed by copying a directory, not resolved by Maven, and Central publishing needs signing keys and an account.
- **Tag releases with the bare Trino version** — matches the existing `467` and `470` tags, but a fix then either replaces the release's archive or needs a suffix added after the fact.
- **Build a release on every push to a version branch** — always current, but publishes unreviewed intermediate states and gives no release a stable name.
- **Publish a Trino container image with ViewZoo installed** — convenient for Kubernetes users, but a second artifact to maintain. It could follow later.

## What this doesn't solve

- A binary's provenance is its tag and the maintainer's machine; no recorded build run exists, and binaries carry no signature or attestation.
- Releasing needs Java 25, Maven, Docker and an authenticated `gh` on that machine.
- Users still need the binary built for exactly their Trino version; versions without a branch get nothing.
- Older branches get no binaries (Rob).
