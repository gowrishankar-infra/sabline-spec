# Provenance

Author: Palakurthi Gowri shankar.

Dates and identifiers for this specification and its reference
implementation. Commit and tag dates are the ones git records, from the
author's clock; the GitHub and Software Heritage records are kept by
those services.

## velaris-spec

| What | Identifier | Date |
|---|---|---|
| Repository | <https://github.com/gowrishankar-infra/velaris-spec> | created on GitHub 2026-09-11T03:29:01Z |
| v0.1, the capability format as first written down, extracted from velaris-lang 3.1.1 (`25d2c051bb5f6925006fed2d44ba8fe809b8cf36`) | annotated tag `v0.1` on commit `f4e7babe7e961d35f6b31450c6d42f3860123acf` | tagged 2026-09-11T08:58:50+05:30 |
| v0.2, tracking velaris-lang 3.3.0 | tag `v0.2` on commit `e45ece9ed6b4bed39a6e884a5cf1d1c343538563` | tagged 2026-09-11T10:28:38+05:30 |
| v0.3, `velaris.capabilities/1` | tag `v0.3` on commit `e2622eb3ba87edd233cdc6fdbfe9113d16bd70d8` | tagged 2026-09-11T13:41:55+05:30 |
| v0.4, the conformance corpus and the predicate type | tag `v0.4` on commit `2bf8bbe189a81582772b5c6549cef6fda18524e2` | tagged 2026-09-11T16:09:41+05:30 |
| v0.5, the producer of the predicate recorded; `counts` and `prover` in `velaris.audit/1` | tag `v0.5` | 2026-09-11 |

## velaris-lang, the reference implementation

velaris-lang (<https://github.com/gowrishankar-infra/velaris-lang>) is
the reference implementation of this specification.

| What | Identifier | Date |
|---|---|---|
| First commit of the effect system: `uses` clauses and the transitive effect checker. It is also that repository's first commit. | `dcb44e2310291fa546405434f4698148413f3cdd` | 2026-08-17T00:21:33+05:30 |
| The version this one tracks | 4.2.0, tag `v4.2.0` | 2026-09-11 |

## Software Heritage

Both repositories were submitted to the Software Heritage archive
through its save-code-now API
(`POST https://archive.softwareheritage.org/api/1/origin/save/git/url/<origin>/`),
twice. The request ids, request dates, visit dates and snapshot
identifiers are the ones the API returned.

The first pair was requested just before velaris-lang 4.1.0 and
velaris-spec 0.4 were pushed, and the archive visited before the push,
so these snapshots hold the history up to velaris-lang 4.0.1 and
velaris-spec 0.3:

| Origin | Save request | Requested (UTC) | Visited (UTC) | Snapshot | `main` in the snapshot |
|---|---|---|---|---|---|
| https://github.com/gowrishankar-infra/velaris-lang | 2471043 | 2026-09-11T10:39:14.948887Z | 2026-09-11T10:39:19.973Z | `swh:1:snp:e4b061fba4098c65f910059d6e3a7c36c7b06e82` | `c080c9f140d06f56a067ff373a09ab89ca76d4c7` (4.0.1) |
| https://github.com/gowrishankar-infra/velaris-spec | 2471044 | 2026-09-11T10:39:16.118803Z | 2026-09-11T10:39:20.075Z | `swh:1:snp:cd54a6a90ef956dcc767b5e3340ff6ad8e18a2a6` | `e2622eb3ba87edd233cdc6fdbfe9113d16bd70d8` (0.3) |

The second pair was requested after the 4.1.0 and 0.4 push; these are
the snapshots taken after it, holding tags `v4.1.0` and `v0.4`:

| Origin | Save request | Requested (UTC) | Visited (UTC) | Snapshot | `main` in the snapshot |
|---|---|---|---|---|---|
| https://github.com/gowrishankar-infra/velaris-lang | 2471049 | 2026-09-11T10:41:21.003154Z | 2026-09-11T10:41:22.251Z | `swh:1:snp:9d8d969d83aac1f1970d5d08ba3755085f28f82c` | `3c81ed1353d3dc1aeec2779329ce59e324f39114` (4.1.0) |
| https://github.com/gowrishankar-infra/velaris-spec | 2471050 | 2026-09-11T10:41:22.084845Z | 2026-09-11T10:41:32.013Z | `swh:1:snp:578ec668186a85ea1eeb8c0a14d77736d3e40186` | `2bf8bbe189a81582772b5c6549cef6fda18524e2` (0.4) |

A save request's record is at
`https://archive.softwareheritage.org/api/1/origin/save/<id>/`, and the
archive's list of each origin's visits at
<https://archive.softwareheritage.org/browse/origin/visits/?origin_url=https://github.com/gowrishankar-infra/velaris-lang>
and
<https://archive.softwareheritage.org/browse/origin/visits/?origin_url=https://github.com/gowrishankar-infra/velaris-spec>.
