# Provenance

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
| v0.4, the conformance corpus and the predicate type | tag `v0.4` | 2026-09-11 |

## velaris-lang, the reference implementation

velaris-lang (<https://github.com/gowrishankar-infra/velaris-lang>) is
the reference implementation of this specification.

| What | Identifier | Date |
|---|---|---|
| First commit of the effect system: `uses` clauses and the transitive effect checker. It is also that repository's first commit. | `dcb44e2310291fa546405434f4698148413f3cdd` | 2026-08-17T00:21:33+05:30 |
| The version this one tracks | 4.1.0, tag `v4.1.0` | 2026-09-11 |

## Software Heritage

Both repositories were submitted to the Software Heritage archive
through its save-code-now API
(`POST https://archive.softwareheritage.org/api/1/origin/save/git/url/<origin>/`).
The request ids and dates are the ones the API returned.

| Origin | Save request id | Requested (UTC) | Status returned | Request |
|---|---|---|---|---|
| https://github.com/gowrishankar-infra/velaris-lang | 2471043 | 2026-09-11T10:39:14.948887+00:00 | accepted; task pending | <https://archive.softwareheritage.org/api/1/origin/save/2471043/> |
| https://github.com/gowrishankar-infra/velaris-spec | 2471044 | 2026-09-11T10:39:16.118803+00:00 | accepted; task pending | <https://archive.softwareheritage.org/api/1/origin/save/2471044/> |

The requests were made just before the commits that add this file were
pushed, so which commit a visit captured depends on when the archive
visited. The archive's own record of each visit and snapshot is at
<https://archive.softwareheritage.org/browse/origin/visits/?origin_url=https://github.com/gowrishankar-infra/velaris-lang>
and
<https://archive.softwareheritage.org/browse/origin/visits/?origin_url=https://github.com/gowrishankar-infra/velaris-spec>.
