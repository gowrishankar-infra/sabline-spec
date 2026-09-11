# velaris-spec

The Velaris capability format, written down so that it can be
implemented without reading the Velaris compiler: the effects a
program may declare, the grammar an operator uses to grant them, what
a runtime must refuse when a program reaches outside its grant, and the
JSON documents that report and record all of it.

**Reference implementation: velaris-lang
(https://github.com/gowrishankar-infra/velaris-lang). Conformance is
defined by the suite in that repository.**

Version 0.3, 2026-09-11. First extracted from velaris-lang 3.1.1;
version 0.2 tracked velaris-lang 3.3.0, which fixed the five defects
the extraction found; version 0.3 tracks velaris-lang 4.0.0, which
reads and writes the baseline of section 9.

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

## What it does not cover

The rest of the Velaris language - types, contracts, proofs, failure -
and time and memory limits. Those are specified by velaris-lang's own
SPEC.md and THREAT_MODEL.md. The format is not a security boundary, and
SPEC.md section 7 lists what a budget does not bound.

## How it stays true to the reference

SPEC.md section 2 quotes velaris-lang SPEC.md sections 6, 7 and 7.1
word for word, and the rest of the document elaborates them.
`tools/check_sync.py` compares the quoted text with velaris-lang's and
fails on any difference; CI runs it on every push and once a week.
Where this text and the reference disagree, that is a bug in one of
them, and until it is fixed the conformance suite decides. Where the
reference does something this text does not settle, SPEC.md says so and
lists it in section 11 as an open question.

## Files

| File | What it is |
|---|---|
| [SPEC.md](SPEC.md) | the specification |
| [schemas/](schemas) | JSON Schema (draft 2020-12) for both documents |
| [examples/audits/](examples/audits) | four `velaris.audit/1` documents produced by velaris-lang 3.1.1, unedited |
| [examples/velaris-lang.capabilities.json](examples/velaris-lang.capabilities.json) | the `velaris.capabilities/1` baseline velaris-lang 4.0.0 writes for those four programs |
| [PRIOR_ART.md](PRIOR_ART.md) | the published work this sits beside, and how it differs |
| [tools/validate.py](tools/validate.py) | checks the schemas, and the examples against them |
| [tools/check_sync.py](tools/check_sync.py) | checks the quoted sections against velaris-lang |
| [CHANGELOG.md](CHANGELOG.md) | versions |

```
pip install jsonschema
python tools/validate.py
python tools/validate.py --audits DIR          # also any audits you produced
python tools/validate.py --capabilities FILE   # also a baseline you committed
python tools/check_sync.py ../velaris-lang/SPEC.md
```

## License

The specification and the schemas are dedicated to the public domain
under [CC0 1.0](LICENSE), so anyone may implement the format, in any
language, under any license. The reference implementation is MIT. See
[NOTICE](NOTICE).
