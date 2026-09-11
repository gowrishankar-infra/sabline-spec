# Changelog

## 0.3 - 2026-09-11

Tracks velaris-lang 4.0.0, which reads and writes the baseline of
section 9. That section stops being provisional.

- **`velaris.capabilities/1`** (SPEC.md 9) replaces the provisional
  `/0`, which no implementation wrote. It records the repository's
  surface - the union of its programs' grants - and for each program
  its grants, a bound on its `fs` and `net` operations in a run, and
  the effects each of its functions declares, or that it does not
  compile; with the producer's version and the date. Schema:
  `schemas/velaris.capabilities.1.schema.json`. The `/0` schema is kept,
  marked superseded.
- **The derivation** (9.3) is stated from the program text: the checks
  that need no prover, then the effects of the file's functions (and of
  an imported `main`), then the paths, hosts and modules its calls name.
  An argument counts as named when it is fixed text - a literal, a
  variable bound once to one, or `+` of two - so moving a literal into
  a variable does not read as a value built while running.
- **The operation bound** (9.4): how many `fs` and `net` operations one
  run can perform, from loops whose counter and limit the text fixes,
  branches, calls and recursion, with no bound where the text sets none.
- **The covering rule** (9.5) compares a path holding a `\` whole: on
  Windows `data/..\..\x` lies outside `data`, and the 0.2 rule let a
  recorded prefix cover it. Q7 notes the change.
- **The comparison** (9.6) is five rules, W1 to W5 - the surface's
  grants and counts, a recorded program's grants and counts, and a
  recorded function's effects - with a table of what widens for each
  kind of scope, what is not a failure, and the rule that a check
  compares with the baseline and with nothing else: not with a previous
  commit. A check that cannot compare must not pass.
- **Q4 resolved** (8.2, 8.4): `velaris.audit/1` gains `ffi_any`, an
  optional field, true when a module is named by a value built while
  running. The audit schema has it.
- **4.6** records that the reference's HTTP door has had an `io` ceiling
  by default since velaris-lang 4.0; **10** adds `check_ratchet.py` to
  the conformance suite and extends the claim to section 9.
- `tools/validate.py` checks examples as `velaris.capabilities/1`,
  including reduction under 9.5, and takes `--capabilities FILE`; CI
  holds velaris-lang's own committed baseline to it.
- Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word
  for word - those sections did not change in 4.0 - so
  `tools/check_sync.py` still passes.

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
