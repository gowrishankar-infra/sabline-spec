# In-toto predicate registry: a pull request, prepared and not sent

**Status: not submitted.** Everything below is ready to send when the
maintainer decides to. Nothing here has been posted to in-toto or
anywhere else.

## Where it would go, and what the process asks

The in-toto Attestation Framework keeps a list of vetted predicate
types in `spec/predicates/README.md` of
<https://github.com/in-toto/attestation>. Its
`docs/new_predicate_guidelines.md`, read on 2026-09-11, asks for a pull
request that:

1. adds the predicate's specification, in the format of
   `spec/predicates/template/template.md` (ITE-9);
2. adds the predicate to the list in `spec/predicates/README.md`;
3. optionally adds a protobuf definition, for the framework's Go,
   Python and Java bindings.

The maintainers review it at their next maintainers meeting. A type URI
under `https://in-toto.io/attestation/` needs a second pull request, to
in-toto.io's redirects; this one is not under that namespace, so it
does not.

## Decide before sending

- **The type URI.** It is
  `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`,
  published on velaris-lang's documentation site, where it resolves to
  the description and the schema. On 2026-09-11 `velaris.dev` resolved
  to a Vercel edge that answered `DEPLOYMENT_NOT_FOUND` for every path,
  and nothing in either repository says who controls that domain, so it
  was not used. A type URI is an identifier: once Statements carry it,
  changing it is a new type. If a different URI is wanted, change it
  before sending, in velaris-spec SPEC.md 8.5, the predicate schema's
  `$id` and `title`, velaris-lang's `build_docs.py`, and this file.
- **The producer.** velaris-lang 4.2.0 writes Statements of this type:
  `velaris attest FILE` writes one, and `velaris attest DIR` one for
  each `.vel` file under DIR, one to a line (JSON Lines). Each
  Statement's `predicate.audit` is `velaris.audit()`'s own output, and
  its subjects are the audited file and its imports by sha256. It signs
  nothing: velaris-lang's EMBEDDING.md gives the commands for cosign
  (`cosign attest-blob --statement`) and for sigstore-python, and its
  release workflow signs one Statement, for `examples/effects.vel`,
  with both and verifies both. The example below is that Statement, as
  is velaris-spec's
  [examples/capability-statement.json](examples/capability-statement.json).
- **Whether to open an issue first.** The guidelines do not require
  one.

## For a reviewer: the artifact, in one command

The Statement for velaris-lang's `examples/effects.vel`, and its two
Sigstore bundles, from the v4.2.0 release (GitHub's `gh`):

    gh release download v4.2.0 --repo gowrishankar-infra/velaris-lang --pattern 'velaris-attestation-*'

or the unsigned Statement alone, with nothing but curl:

    curl -LO https://github.com/gowrishankar-infra/velaris-lang/releases/download/v4.2.0/velaris-attestation-4.2.0.intoto.json

To write it on your own machine instead, with git and Python 3.10 or
later (`velaris.py` needs nothing else):

    git clone -q --depth 1 --branch v4.2.0 https://github.com/gowrishankar-infra/velaris-lang && cd velaris-lang && SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) python velaris.py attest examples/effects.vel --output effects.intoto.json

With the optional prover installed (`pip install z3-solver`), as the
release workflow has it, the file is byte for byte the release's
`velaris-attestation-4.2.0.intoto.json`; without it the audit's
`prover` is `false`, and nothing else differs.

To check the cosign bundle against the example's bytes and the
release workflow's identity, in that clone:

    cosign verify-blob-attestation --bundle velaris-attestation-4.2.0.cosign.sigstore.json --type https://gowrishankar-infra.github.io/velaris-lang/capability/v1 --certificate-identity https://github.com/gowrishankar-infra/velaris-lang/.github/workflows/release.yml@refs/tags/v4.2.0 --certificate-oidc-issuer https://token.actions.githubusercontent.com examples/effects.vel

## The pull request

**Title:** Add predicate type: Velaris capability (velaris.audit/1)

**Body:**

> This adds a predicate type for a Velaris program's capability
> surface: a `velaris.audit/1` document - the effects a program
> declares, the paths, hosts and modules it names, and the narrowest
> budget to run it under - bound to the digests of the source files it
> describes.
>
> **Use case.** Code written by a model is increasingly run without
> being read line by line. Velaris is a small language in which each
> function declares its effects, checked transitively, and a runtime
> refuses any effect outside the budget its operator grants. Its audit
> says, before a program runs, what the program may do. On its own the
> audit names no file and carries no signature, so a consumer cannot
> tell which source it describes or who produced it. As an in-toto
> predicate, a signed Statement says: this producer read these bytes
> and reports this surface.
>
> **Why existing predicates do not cover it.** SLSA Provenance records
> how an artifact was built, not what a source file may do. Test Result
> and Simple Verification Result record the outcome of running tests or
> policies, not a program's declared surface. A SCAI Report can assert
> that an artifact has an attribute and point at evidence, but does not
> define the attribute's content; a policy would have to parse the
> evidence by convention. This predicate has a schema, so a policy can
> read `effects`, `net_hosts` or `safe_command` directly.
>
> **Policy questions it answers.** Does this program declare `net`, or
> `ffi`? Does it name only hosts on an allow-list? Is the budget it
> needs within what this environment grants? Did the audit compile
> (`ok`)? Which producer wrote it, and which version of the format did it
> follow?
>
> **Producer.** velaris-lang 4.2.0 writes Statements of this type
> (`velaris attest`), unsigned; its releases carry one for an example
> program, signed with cosign and with sigstore-python.
>
> **What it does not claim.** That the audit is right, that the program
> is safe, or that any runtime will enforce the budget. The format is
> specified, under CC0, at <https://github.com/gowrishankar-infra/velaris-spec>
> (section 8.5 for this predicate); its reference implementation is
> <https://github.com/gowrishankar-infra/velaris-lang>.

## The line for `spec/predicates/README.md`

In the list under "Vetted Predicates", in alphabetical order:

```markdown
-   [Velaris Capability]: The capability surface a Velaris program
    declares, as a velaris.audit/1 document bound to its source files.
```

and among the link definitions:

```markdown
[Velaris Capability]: velaris-capability.md
```

## `spec/predicates/velaris-capability.md`

The whole file, to add as it stands:

~~~~markdown
# Predicate type: Velaris Capability

Type URI: https://gowrishankar-infra.github.io/velaris-lang/capability/v1

Version: 1.0.0

Predicate Name: Velaris Capability

Authors: Palakurthi Gowri Shankar (@gowrishankar-infra)

## Purpose

To say, in a signed statement, what a program written in Velaris may do
to the world outside it - which of seven effects it declares, which
paths, hosts and Python modules it names, and the narrowest budget to
run it under - and which source files that description is of. The
description is a `velaris.audit/1` document, defined by velaris-spec
(<https://github.com/gowrishankar-infra/velaris-spec>, section 8); this
predicate binds it to the digests of the files audited.

## Use Cases

### Deciding whether to run agent-written code

A model writes a Velaris program. Before it runs, a pipeline audits it
and signs the Statement. The environment that runs it verifies the
signature, checks that the first subject's digest is the file it is
about to run, and applies a policy to the predicate: no `ffi`, no
`net` except hosts on an allow-list, a `safe_command` within the budget
the environment grants. It then runs the program under that budget,
which the Velaris runtime enforces at each operation.

### Recording what changed in a review

A repository audits each changed `.vel` file on a pull request and
attaches the Statements to the pull request's commit. A later reader
can see what each file declared at that commit, and that the audit was
of those bytes.

Existing predicates record how an artifact was built (SLSA Provenance),
the result of running tests or policies (Test Result, Simple
Verification Result), or an attribute asserted with evidence by
reference (SCAI). None defines the content of a program's declared
capability surface, which a policy needs to read field by field.

## Prerequisites

The in-toto Attestation Framework, Statement v1. The Velaris capability
format, velaris-spec version 0.4 or later: section 8 defines
`velaris.audit/1` and section 8.5 this predicate. A producer is an
implementation of that format; level L1 of velaris-spec
CONFORMANCE.md is the level that covers writing audits. The reference
implementation is velaris-lang
(<https://github.com/gowrishankar-infra/velaris-lang>).

## Model

The producer is the tool that audits the source - in the reference
implementation, `velaris attest`, which puts `velaris audit`'s document
in a Statement - run by whoever audits it and signed by them: a CI job, a
review bot, an agent platform before it runs a program. The consumer
is whatever decides whether to run the program, or records that it was
reviewed. The predicate describes source text, before any build and
before any run.

## Schema

```jsonc
{
  // Standard attestation fields:
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    {"name": "<the audited file>", "digest": {"sha256": "<hex>"}},
    {"name": "<a file it imports>", "digest": {"sha256": "<hex>"}}
  ],

  // Predicate:
  "predicateType": "https://gowrishankar-infra.github.io/velaris-lang/capability/v1",
  "predicate": {
    "producer": {"name": "<implementation>", "uri": "<optional>"},
    "specification": "velaris-spec 0.5",          // optional
    "auditedAt": "<RFC 3339, Z>",                  // optional
    "conformance": {"levels": ["L1"], "corpus": "<optional>"},  // optional
    "audit": { /* a velaris.audit/1 document */ }
  }
}
```

JSON Schema for the predicate:
<https://gowrishankar-infra.github.io/velaris-lang/capability/v1/schema.json>.
The audit's own schema:
<https://github.com/gowrishankar-infra/velaris-spec/blob/main/schemas/velaris.audit.1.schema.json>.

### Parsing Rules

This predicate follows the framework's standard parsing rules,
including the monotonic principle. A consumer MUST ignore fields it
does not know, in the predicate and in the audit, whose own rule is the
same (velaris-spec 8.1). Fields may be added within v1; a change of
meaning is a new type URI, `.../capability/v2`. The first subject MUST
be the audited file; a consumer MUST check its digest against the file
it means to trust. The producer MUST have produced the audit from
exactly the bytes the subjects' digests name. When `audit.ok` is false
the predicate asserts nothing about what the program may do.

### Fields

`producer` _object, required_

The implementation that wrote the audit: `name` (string, required) and
`uri` (string, optional). Its version is `audit.velaris_version`.

`audit` _object, required_

A `velaris.audit/1` document for the first subject, as velaris-spec
section 8 defines it: among other fields `ok`, `effects` (a subset of
`io`, `env`, `fs`, `net`, `clock`, `rand`, `ffi`), `functions`,
`ffi_modules`, `ffi_any`, `fs_paths`, `net_hosts`, `safe_command` and,
from velaris-spec 0.5, `counts` (a bound on file and network
operations, `null` where none is determined) and `prover`. Where the
audit could not determine something it says so in these fields -
`ok` false, `ffi_any`, `fs_paths.read_any`, `net_hosts.any`, a `null`
count - and the predicate carries them unchanged.

`specification` _string, optional_

The velaris-spec version the producer followed, as `velaris-spec 0.5`.

`auditedAt` _string ([Timestamp]), optional_

When the audit was made, in UTC, by the producer's clock.

`conformance` _object, optional_

The conformance levels of velaris-spec CONFORMANCE.md the producer
claims (`levels`, any of `L1`, `L2`, `L3`) and the corpus it ran
(`corpus`). A claim, not evidence.

The Statement's `subject`: the audited file first, then, where the
producer lists them, the files it imports, each with a `sha256` digest.

[Timestamp]: ../v1/field_types.md#Timestamp

## Example

The Statement velaris-lang 4.2.0 writes for `examples/effects.vel` in
that repository (`velaris attest examples/effects.vel`), before it is
signed. It has no `conformance` field: `velaris attest` does not run
the conformance corpus, so it claims no level.

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    {
      "name": "examples/effects.vel",
      "digest": {
        "sha256": "e483365ce74a20770a1ef503f185f4de2c16b0524797408784a235e78b6baafb"
      }
    }
  ],
  "predicateType": "https://gowrishankar-infra.github.io/velaris-lang/capability/v1",
  "predicate": {
    "producer": {
      "name": "velaris-lang",
      "uri": "https://github.com/gowrishankar-infra/velaris-lang"
    },
    "specification": "velaris-spec 0.5",
    "auditedAt": "2026-09-11T14:20:49Z",
    "audit": {
      "schema": "velaris.audit/1",
      "velaris_version": "4.2.0",
      "ok": true,
      "problems": [],
      "effects": [
        "clock",
        "fs",
        "io",
        "rand"
      ],
      "functions": [
        {
          "name": "dice",
          "effects": [
            "rand"
          ],
          "can_fail": false,
          "requires": [],
          "ensures": [],
          "status": "no promises",
          "loops_unshown": 0
        },
        {
          "name": "timestamp",
          "effects": [
            "clock"
          ],
          "can_fail": false,
          "requires": [],
          "ensures": [],
          "status": "no promises",
          "loops_unshown": 0
        },
        {
          "name": "save_report",
          "effects": [
            "fs"
          ],
          "can_fail": false,
          "requires": [],
          "ensures": [],
          "status": "no promises",
          "loops_unshown": 0
        },
        {
          "name": "main",
          "effects": [
            "clock",
            "fs",
            "io",
            "rand"
          ],
          "can_fail": false,
          "requires": [],
          "ensures": [],
          "status": "no promises",
          "loops_unshown": 0
        }
      ],
      "proven_share": null,
      "safe_command": "velaris <file> --allow clock,fs:read:report.txt,fs:write:report.txt,io,rand",
      "warnings": [],
      "ffi_modules": [],
      "loops_unshown": 0,
      "contract_coverage": [],
      "fs_paths": {
        "read": [
          "report.txt"
        ],
        "write": [
          "report.txt"
        ],
        "read_any": false,
        "write_any": false
      },
      "net_hosts": {
        "hosts": [],
        "any": false
      },
      "ffi_any": false,
      "counts": {
        "fs": 2,
        "net": 0
      },
      "prover": true
    }
  }
}
```

## Changelog and Migrations

Version 1.0.0: the first version.
~~~~

## `protos/in_toto_attestation/predicates/velaris_capability/v1/velaris_capability.proto` (optional)

```proto
syntax = "proto3";

package in_toto_attestation.predicates.velaris_capability.v1;

import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";

option go_package = "github.com/in-toto/attestation/go/predicates/velaris_capability/v1";
option java_package = "io.github.intoto.attestation.predicates.velaris_capability.v1";

message Producer {
    string name = 1;
    string uri = 2;
}

message Conformance {
    repeated string levels = 1;
    string corpus = 2;
}

message VelarisCapability {
    Producer producer = 1;
    string specification = 2;
    google.protobuf.Timestamp audited_at = 3;
    Conformance conformance = 4;
    // a velaris.audit/1 document; its schema is velaris-spec's
    // schemas/velaris.audit.1.schema.json
    google.protobuf.Struct audit = 5;
}
```
