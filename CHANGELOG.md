# Changelog

## 0.2 - 2026-09-11

Tracks velaris-lang 3.3.0, which fixed the five defects the 0.1
extraction found and recorded. The format text is revised where the
behaviour changed, and the five open questions those fixes close are
resolved.

- **Q1 resolved** (SPEC.md 3.2): an unknown name in a `uses` clause is a
  compile error naming the seven effects, so `velaris.audit/1`'s
  `effects` is always a subset of them.
- **Q2 resolved** (SPEC.md 4.3): `ffi` grants are additive like `fs` and
  `net` - a plain `ffi` grants every module and the wider grant wins, so
  `ffi,ffi:math` grants every module. The reference text's "Grants are
  additive" now describes `ffi` too.
- **Q3 resolved** (SPEC.md 8): the command line's `audit --json` emits
  `velaris.audit/1`, the same document as every other door, so the
  schema no longer rejects it; its `safe_command` for
  `examples/json_ffi.vel` is `ffi:math,io`.
- **Q5 resolved** (SPEC.md 5.1, 5.2, 8.2, 8.3, 8.4): an IPv6 host is
  written in brackets in the grammar, in `net_hosts` and in
  `safe_command`, and `, @ [ ] %` are percent-encoded inside a path or
  host component and decoded when the budget is parsed. `safe_command`
  round-trips. This changes what the `net_hosts` field holds for an IPv6
  host, which is why it is made in a new format version rather than
  within version 1.
- **Q6 resolved** (SPEC.md 4.2, 5.3): a count is ASCII digits only, and
  `ffi:M@N` and `ffi:` with no module are budget errors; no malformed
  budget produces a traceback.
- **SPEC.md 5.3** now states the attribute-chain bound: an `ffi:M` grant
  covers the whole dotted path a call reaches, not only the module it
  names, closing the dotted-path part of Q9. The escaping rule is added
  to 5.1 and 5.2. Q9 notes the rules the suite now covers.
- The two JSON Schemas' `$id` values point at the `v0.2` tag. Their shape
  is unchanged; the descriptions of `net_hosts` and `effect_name` note
  what 3.3.0 changed, and both still accept documents from earlier
  producers.
- Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word
  for word - those sections did not change, since "grants are additive"
  is now true for `ffi` too - so `tools/check_sync.py` still passes, and
  `tools/validate.py` still passes against the examples.

## 0.1 - 2026-09-11

First version, extracted from velaris-lang 3.1.1 (commit `25d2c05`).

- SPEC.md: the seven effects and the transitive rule; the grant grammar
  as the reference parses it, including the forms the reference text
  does not mention; how `fs`, `net` and `ffi` grants are resolved and
  matched; counts; the order in which a runtime checks an operation;
  what a budget does not bound; `velaris.audit/1` field by field;
  `velaris.capabilities/0`; conformance; eleven open questions.
- Section 2 of SPEC.md quotes velaris-lang SPEC.md sections 6, 7 and
  7.1 word for word; `tools/check_sync.py` fails if they drift.
- `schemas/velaris.audit.1.schema.json`, validated against the
  `velaris.audit/1` output of velaris-lang 3.1.1 for each of the 107
  `.vel` files in that repository's `examples/` and `stdlib/`
  directories, those that compile and those built to be refused. It
  does not accept the
  output of `velaris audit FILE --json`, which in 3.1.1 is a different,
  unversioned shape (SPEC.md section 8, open question Q3).
- `schemas/velaris.capabilities.0.schema.json`, provisional: the
  reference implementation does not read or write baselines yet.
- Found while extracting, and recorded in SPEC.md rather than smoothed
  over: the reference restricts `ffi` to named modules when `ffi` and
  `ffi:M` both appear, where its own text says grants are additive
  (Q2); an `ffi:M` grant checks the module name a call gives, and not
  what is reachable through that module's attributes (section 5.3);
  the audit's `safe_command` is wrong for IPv6 hosts and for paths
  containing `,` or `@` (Q5); any identifier is accepted in `uses` (Q1).
