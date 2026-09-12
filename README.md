# velaris-spec

The Velaris capability format, written down so that it can be
implemented without reading the Velaris compiler: the effects a
program may declare, the grammar an operator uses to grant them, what
a runtime must refuse when a program reaches outside its grant, and the
JSON documents that report and record all of it.

**Reference implementation: velaris-lang
(https://github.com/gowrishankar-infra/velaris-lang). Conformance is
defined by the corpus in [tests/](tests), at the three levels of
[CONFORMANCE.md](CONFORMANCE.md).**

Version 0.6.0, 2026-09-12. First extracted from velaris-lang 3.1.1;
version 0.2 tracked velaris-lang 3.3.0, which fixed the five defects
the extraction found; version 0.3 tracked velaris-lang 4.0.0, which
reads and writes the baseline of section 9; version 0.4 tracked
velaris-lang 4.1.0, and added the conformance corpus and an in-toto
predicate type; version 0.5 tracked velaris-lang 4.2.0, which writes
Statements of that type (`velaris attest`); versions 0.5.1 and 0.5.2
tracked velaris-lang 4.2.1; version 0.5.3 tracked velaris-lang 4.3.2,
and none of those three changed a rule. Version 0.6.0 tracks
velaris-lang 5.0.0, which made `io` - the console alone - the budget a
run gets when nobody writes one, where it used to be all seven
effects: sections 4.4 and 4.6 are restated.

## What it covers

- **Effects** - `io`, `env`, `fs`, `net`, `clock`, `rand`, `ffi` - and
  the rule that a function's declaration covers every call it can make,
  at any depth ([SPEC.md](SPEC.md) section 3).
- **The grant grammar**: `fs:read:./data`, `net:api.example.com:443`,
  `net:*.example.com`, `ffi:math`, `@100` - parsed, resolved and
  matched exactly as the reference does it, edge cases included
  (sections 4 and 5).
- **What a budget guarantees at runtime, and what it does not**
  (sections 6 and 7).
- **`velaris.audit/1`**: the JSON report of what a program declares and
  names before it runs (section 8,
  [schemas/velaris.audit.1.schema.json](schemas/velaris.audit.1.schema.json)).
- **`velaris.capabilities/1`**: the baseline in which a repository
  declares the capability surface its programs may have - their
  grants, a bound on their file and network operations, each
  function's effects - and the comparison that fails a change which
  needs more, made against that baseline and never against the
  previous commit, so capability added a little at a time is caught
  as surely as all at once (section 9,
  [schemas/velaris.capabilities.1.schema.json](schemas/velaris.capabilities.1.schema.json)).
  From 0.3 it is not provisional: the reference implementation writes
  it (`velaris capabilities init`) and checks against it (`velaris
  capabilities check`). The provisional `/0` form of 0.1 and 0.2 is
  superseded; its schema is kept for the record.
- **An in-toto predicate type** for `velaris.audit/1`,
  `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`, so
  a signed statement can say which source files an audit describes
  (section 8.5, [schemas/capability-predicate.v1.schema.json](schemas/capability-predicate.v1.schema.json)).
  From 0.5 the reference implementation writes such statements
  (`velaris attest`), unsigned, and its releases carry one signed with
  cosign and with sigstore-python.
- **Conformance** at three levels - L1 Declaration, L2 Enforcement, L3
  Ratchet - defined by a corpus of 444 JSON cases that an
  implementation in any language runs its own way, with a runner
  contract ([CONFORMANCE.md](CONFORMANCE.md), [tests/](tests)). No level
  needs a theorem prover.

## What it does not cover

The rest of the Velaris language - types, contracts, proofs, failure -
and time and memory limits. Those are specified by velaris-lang's own
SPEC.md and THREAT_MODEL.md. The format is not a security boundary, and
SPEC.md section 7 lists what a budget does not bound.

## How it stays true to the reference

SPEC.md section 2 quotes velaris-lang SPEC.md sections 6, 7 and 7.1
word for word, and the rest of the document elaborates them.
`tools/check_sync.py` compares the quoted text with velaris-lang's, and
the predicate schema with the copy velaris-lang publishes, and fails on
any difference. The corpus in `tests/` is written by velaris-lang's
`build_conformance.py` from the tables of three of its suites, which
assert the same expectations against velaris-lang; a drift test
regenerates it and fails when it differs from what is committed here.
CI runs all of it on every push and once a week, and runs velaris-lang
against the corpus. Where this text and the reference disagree, that is
a bug in one of them, and until it is fixed the corpus decides. Where
the reference does something this text does not settle, SPEC.md says so
and lists it in section 11 as an open question.

## Files

| File | What it is |
|---|---|
| [SPEC.md](SPEC.md) | the specification |
| [CONFORMANCE.md](CONFORMANCE.md) | the three levels of conformance, the behaviours each requires, and how to claim one |
| [tests/](tests) | the conformance corpus: 444 cases, the runner contract ([tests/README.md](tests/README.md)) and the case schema |
| [schemas/](schemas) | JSON Schema (draft 2020-12) for both documents and for the predicate |
| [examples/audits/](examples/audits) | four `velaris.audit/1` documents produced by velaris-lang 3.1.1, unedited |
| [examples/velaris-lang.capabilities.json](examples/velaris-lang.capabilities.json) | the `velaris.capabilities/1` baseline velaris-lang 4.0.0 writes for those four programs |
| [examples/capability-statement.json](examples/capability-statement.json) | an in-toto Statement of the predicate type: what `velaris attest examples/effects.vel` writes at velaris-lang v4.2.0 |
| [PRIOR_ART.md](PRIOR_ART.md) | the published work this sits beside, and how it differs |
| [REGISTRY_SUBMISSION.md](REGISTRY_SUBMISSION.md) | the pull request listing the predicate type with in-toto: its branch is pushed, and the steps left before it is opened |
| [MCP_PROPOSAL.md](MCP_PROPOSAL.md) | a draft, not sent: a capability declaration for Model Context Protocol tools |
| [NIST_SUBMISSION.md](NIST_SUBMISSION.md) | a draft, not sent: input to NIST's AI Agent Standards Initiative |
| [CATALOGUE_SUBMISSION.md](CATALOGUE_SUBMISSION.md) | a draft, not sent: an entry for the agentlanguages.dev catalogue, and what it asks of one |
| [PROVENANCE.md](PROVENANCE.md) | dates and archive identifiers |
| [CITATION.cff](CITATION.cff) | how to cite this repository |
| [tools/validate.py](tools/validate.py) | checks the schemas, the examples and the corpus |
| [tools/check_sync.py](tools/check_sync.py) | checks the quoted sections and the predicate schema against velaris-lang |
| [CHANGELOG.md](CHANGELOG.md) | versions |

```
pip install jsonschema
python tools/validate.py
python tools/validate.py --audits DIR          # also any audits you produced
python tools/validate.py --capabilities FILE   # also a baseline you committed
python tools/check_sync.py ../velaris-lang/SPEC.md
python ../velaris-lang/build_conformance.py --check tests   # the drift test
python ../velaris-lang/velaris.py conformance --corpus tests
```

## Cite this repository

The author is Palakurthi Gowri Shankar (family name Palakurthi).
[CITATION.cff](CITATION.cff) holds the citation, and GitHub offers it as
"Cite this repository" beside the file list. A preprint describing
Velaris and this format is forthcoming; until it is published, cite the
repository. [PROVENANCE.md](PROVENANCE.md) records the dates and the
archive identifiers.

## License

The specification and the schemas are dedicated to the public domain
under [CC0 1.0](LICENSE), so anyone may implement the format, in any
language, under any license. The reference implementation is MIT. See
[NOTICE](NOTICE).
