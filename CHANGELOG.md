# Changelog

## 0.6.0 - The default budget is io, not all seven effects - 2026-09-12

Tracks velaris-lang 5.0.0. Two sections are restated and one
conformance case is rewritten; the corpus is still 444 cases, and no
effect, grant, refusal code, schema or field changes.

**4.6, when no budget is given.** Until velaris-lang 5.0 the
reference's command line (`velaris file.vel`), library
(`velaris.run(source)` with no `allow`) and worker pool granted all
seven effects, unscoped, and this section said so. From 5.0 all three
grant `io` - print, read a line, and the command-line arguments - as
the MCP server and the HTTP door already did, so every place a budget
comes from in the reference answers the same way. What a runtime does
with no budget is still outside this format, and the SHOULD is
unchanged: require an explicit budget, or default to one that grants
no more than `io`. The reference now satisfies it.

**4.4, denials.** The old text said that when no grants are given a
denial starts from all seven effects, unscoped. That tied the denial
algorithm to one runtime's default, and the reference's default has
now changed. It says instead that a denial narrows the runtime's
default budget, which 4.6 leaves to the runtime, and that a
conformance case always writes the grants its denial applies to.

**The corpus.** `L1-budget-deny-from-all-seven`, which denied `net`
and `ffi` with no grants and expected the other five, becomes
`L1-budget-deny-from-grants-given`, which grants all seven in its own
text and denies the same two, expecting the same five: the same
algorithm, stated without reference to any default. `L2-deny-one` and
`L2-deny-several` gain the grants their denials remove from, so no
case's outcome depends on an implementation's default any more. Five
cases in the reference's own suites assert the new default and the
refusal it produces; all five are recorded in `tests/index.json` as
excluded, because the default is the runtime's choice and the
refusal's wording is not stable.

**`--allow all`** is the reference's command-line shorthand for the
seven effects, and prints one line to standard error when an operator
uses it. It is not part of the grammar of sections 4 and 5: a budget a
caller sends to the HTTP door or the MCP server cannot contain it, and
no case parses it.

## 0.5.3 - 2026-09-12

Tracks velaris-lang 4.3.2. No rule, field, schema or conformance case
changes; the corpus is still 444 cases.

velaris-lang has had three releases since 0.5.2 was written against
4.2.1: 4.3.0 added `Money of CUR`, an exact decimal whose `split` is
proven to add back up; 4.3.1 made a proof that exhausts its time say
so rather than fall silently back to a runtime check; and 4.3.2
corrected the language card's stated size and rewrote the MCP registry
manifest for that registry's current schema. None of the three touches
the capability format - no effect, no grant, no refusal code, no field
of `velaris.audit/1` or `velaris.capabilities/1`, and no case of the
corpus. This version therefore changes only the places that name the
reference implementation's current release: SPEC.md's header and its
"The reference" convention, README.md, CONFORMANCE.md's version and
its claim template, CITATION.cff, PROVENANCE.md and the statement of
what the reference implementation is in NIST_SUBMISSION.md.

Statements about when a feature arrived - "velaris-lang 4.2.0 and
later write such Statements", "From velaris-lang 4.2.0 the reference
implementation writes Statements of the type" - are history and are
left alone, as are the `v4.2.0` artifacts in REGISTRY_SUBMISSION.md's
verification recipe, which names a specific release on purpose.

## 0.5.2 - 2026-09-11

Tracks velaris-lang 4.2.1. No rule, field, schema or conformance case
changes; the corpus is still 444 cases.

- **MCP_PROPOSAL.md**, a draft, not sent: an optional capability
  declaration for Model Context Protocol tools, written against the MCP
  specification revision 2026-07-28. It carries grants in this
  format's grammar in a namespaced `_meta` key, uses section 9.5's
  covering rule for a client to notice a declaration that has widened
  since it was approved, gives two tools of velaris-lang's MCP server
  as examples, says what would enforce a declaration and what it does
  not solve, and names the MCP proposals it overlaps (SEP-3140,
  SEP-1076).
- **NIST_SUBMISSION.md**, a draft, not sent: input to NIST's AI Agent
  Standards Initiative. Every call for input the Initiative has made
  closed by 2026-04-02, and it records that; it is written as a general
  submission for the next one.
- **REGISTRY_SUBMISSION.md**: the in-toto pull request's branch is
  pushed (gowrishankar-infra/attestation, `velaris-capability-predicate`)
  and not opened. in-toto's AI policy asks that the pull request's
  description be written by the submitter and that only the submitter
  sign off for the DCO, so those steps are left to the maintainer, with
  what the description has to state. The reviewer's verification now
  downloads the example file's bytes instead of checking it out, because
  a checkout that converts line endings changes its digest; run on
  2026-09-11 with cosign v3.0.6, it verifies for v4.2.0 and v4.2.1.

## 0.5.1 - 2026-09-11

Tracks velaris-lang 4.2.1. A text change only: no rule, field, schema
or conformance case changes.

- The author's name is written with a capital S: Palakurthi Gowri
  Shankar - family name Palakurthi, given name Gowri Shankar - in
  CITATION.cff (`given-names: Gowri Shankar`, in the author and in the
  reference to velaris-lang), NOTICE, README.md, PROVENANCE.md and
  REGISTRY_SUBMISSION.md. Abbreviated, it is "Palakurthi, G. S." in
  APA and BibTeX's apalike, and "G. S. Palakurthi" in IEEE. The entry
  for 0.5 below keeps the form 0.5 used.
- The schemas' `$id` values still point at the `v0.5` tag, whose
  schemas are the same files.

## 0.5 - 2026-09-11

Tracks velaris-lang 4.2.0, which writes Statements of the predicate
type 0.4 defined.

- **Section 8.5** records the producer. `velaris attest FILE` writes one
  in-toto Statement v1: its subjects are the file and each file it
  imports, by the sha256 of the bytes the audit read, and its
  `predicate.audit` is the reference's `audit()` output itself, so it
  holds nothing the audit does not. `velaris attest DIR` writes one
  Statement per program, as JSON Lines. It signs nothing; the
  reference's release workflow signs one Statement with cosign and with
  sigstore-python and verifies both.
- **`velaris.audit/1`** gains two optional fields within version 1
  (section 8.2 and the schema): `counts`, the bound of section 9.4 on
  the `fs` and `net` operations of the functions the audited file
  defines - `null` for an effect whose bound the text does not fix, and
  `null` as a whole when no bound was determined, as when `ok` is false;
  and `prover`, whether a prover decided the promises' status. Section
  8.4 says what a count is not.
- **examples/capability-statement.json** is the Statement `velaris
  attest examples/effects.vel` writes at velaris-lang v4.2.0, with
  `SOURCE_DATE_EPOCH` at that commit's time, as the release workflow
  writes it. 0.4's was assembled by hand.
- **REGISTRY_SUBMISSION.md** names the producer and the command that
  fetches the signed Statement, and its example is the real one. It is
  still not submitted.
- The predicate type, its URI and its schema are unchanged, as are the
  corpus (444 cases) and section 2, so `tools/check_sync.py` still
  passes. The three schemas' `$id` values point at the `v0.5` tag.
- The author's name is written in full, family name first:
  Palakurthi Gowri shankar (family name Palakurthi, given name Gowri
  shankar), in CITATION.cff, NOTICE, README.md, PROVENANCE.md and
  REGISTRY_SUBMISSION.md.

## 0.4 - 2026-09-11

Tracks velaris-lang 4.1.0. Conformance becomes something an
implementation can run, and the audit gets a predicate type.

- **CONFORMANCE.md** defines three levels. L1 Declaration: parse the
  budget grammar, check declarations, compute a program's effect
  surface and emit `velaris.audit/1` that validates. L2 Enforcement:
  refuse at run time every operation outside the budget, with the code
  G2 gives it, uncatchably. L3 Ratchet: write and read
  `velaris.capabilities/1` and classify widening and narrowing for every
  kind of scope. L2 and L3 each need L1; L3 does not need L2. No level
  needs a theorem prover. Each level lists the behaviours it requires
  and the cases that test them, and says what no case tests yet.
- **tests/** is the conformance corpus: 444 JSON cases - 298 at L1
  (280 budgets, 18 audits), 37 at L2 (runs under a budget, with a
  fixture of files and two local HTTP servers) and 109 at L3
  (derivations, checks, two sequences, the write guard, the covering
  rule, reduction, operation bounds), 5 of them recording the ratchet's
  known limits with the outcome the reference gives today.
  `tests/README.md` is the runner contract; `tests/case.schema.json`
  checks a case's shape; `tests/index.json` lists every case and the 13
  scenarios left out, with why - six that depend on Python's object
  model, four that need a Python host, a run given no budget, and two
  about the reference's command line.
- The corpus is **written by velaris-lang's `build_conformance.py`** from
  the tables of `check_sandbox.py`, `check_library.py` and
  `check_ratchet.py`, which assert the same entries against velaris-lang.
  CI here, and in velaris-lang, regenerates it and fails when it
  differs from what is committed, and runs velaris-lang against it.
- **Section 10** is rewritten around the corpus; **Q8** (a harness for
  other languages) and **Q9** (rules the suite did not test) are
  resolved - the four rules 0.3 listed as untested are cases now.
- **Section 8.5** defines an in-toto predicate type,
  `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`,
  for `velaris.audit/1` bound to the digests of the files audited,
  with `schemas/capability-predicate.v1.schema.json` and an example
  Statement in `examples/`. The URL resolves: velaris-lang publishes the
  description and the same schema there, and `tools/check_sync.py` fails
  if the two schemas differ. **Q11** is resolved. REGISTRY_SUBMISSION.md
  holds a pull request, prepared and not sent, listing the type with
  in-toto.
- **Corrected: sections 3.2, 8.2 and 8.3** said that an audit's
  `effects` is always a subset of the seven effects and that
  `safe_command` always parses. Neither was true of the audit of a
  program refused for naming an unknown effect: from velaris-lang
  3.3.0 to 4.0.1 it listed the name in `effects` and in `safe_command`.
  Writing the corpus found it; velaris-lang 4.1.0 leaves the name out,
  and the sections now say what holds, and require it.
- PRIOR_ART.md: the SARIF entry said the reference emits no SARIF,
  which stopped being true in velaris-lang 3.4; the in-toto entry
  describes the predicate type; a new entry places the ratchet beside
  Hills, Caspary and Cooper Stickland's "Distributed Attacks in
  Persistent-State AI Control" (2026), without claiming it as a source.
- CITATION.cff and PROVENANCE.md are added; NOTICE covers the corpus.
- The JSON Schemas' `$id` values point at the `v0.4` tag. Section 2
  still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word for
  word - they did not change in 4.1 - so `tools/check_sync.py` passes.

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
