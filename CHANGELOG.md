# Changelog

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
