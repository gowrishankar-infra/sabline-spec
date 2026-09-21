# Changelog

The reference implementation was called **Velaris** until
0.14.0 / sabline-lang 8.6.0; every entry below 0.14.0 uses the
name it had at the time.

## 0.14.0 - The reference implementation is renamed - 2026-09-20

Tracks sabline-lang 8.6.0. The reference implementation was called
**Velaris** and is now called **Sabline**: the name belongs to an unrelated
company in the same market (velaris.io), and was given up rather than
contested. This document is renamed with it. Nothing else changed - no
rule of any section, no field of any document, no conformance case.

Additive: every document valid under 0.13.0 is valid under 0.14.0 and means
the same, and an implementation that reads 0.13.0's names goes on reading
them.

- **The document formats are `sabline.*`** where they were `velaris.*`:
  `sabline.audit/1`, `sabline.capabilities/1`, `sabline.capabilities/0`,
  `sabline.receipt/1` and the rest (section 8). A producer MUST write the
  `sabline.*` name. A consumer SHOULD read the `velaris.*` name of the same
  document at the same version as that document - it is a rename, not a new
  version - and MUST NOT read it as anything else. The schemas in
  `schemas/` are renamed to match; their contents are otherwise byte for
  byte what 0.13.0 published.
- **Both predicate types are named at sabline.dev** (sections 8.5 and 8.7):
  `https://sabline.dev/capability/v1` and `https://sabline.dev/receipt/v1`.
  Each has now been named at three addresses, and a consumer SHOULD read
  all three as the same type: the new one, `velaris-lang.dev` (0.11.0 to
  0.14.0, written by sabline-lang 8.3.0 to 8.5.0), and the reference's
  GitHub Pages address (until 0.11.0, written by 4.2.0 to 8.2.1). Nothing
  is ever removed from that list; a name that was published and signed goes
  on being accepted. Both earlier addresses redirect to sabline.dev.
  Neither `velaris.dev` nor `velaris.io` has ever been this document's
  domain, and neither names any type it defines.
- **The repository is `gowrishankar-infra/sabline-spec`**, renamed in
  place, so the old URL redirects. The reference implementation is
  `gowrishankar-infra/sabline-lang`, on PyPI and npm as `sabline-lang`.
- **The conformance corpus is unchanged**: 456 cases, the same ids, the
  same expectations. A case names no implementation.
- **`velaris_version` is kept, and `sabline_version` added beside it**, in
  `sabline.audit/1` and `sabline.capabilities/1`. It is the one field whose
  name carried the project's. Renaming it would have made a required field
  disappear from a version-1 document, which section 8's own rule forbids -
  within a version fields may be added, and none changes meaning or
  disappears without the `schema` value changing. So a producer writes both
  with the same value, and a consumer may read either. The schemas require
  *one of the two* rather than a named one, which is the actual rule: a
  document written before 0.14.0 carries the old name, one written by the
  reference from 8.6.0 carries both, and one written by an implementation
  that never knew the old name carries the new. A document carrying neither
  is refused. `velaris_version` goes in a version that says so.

  The documents in `examples/` keep `velaris_version` alone: each records
  what a particular release wrote - 3.1.1, 4.0.0, 4.2.0 - and those wrote
  that name and no other.

  The schemas accept both names for the format itself, too: each `schema`
  field is an `enum` of the `sabline.*` name and the `velaris.*` one where
  it was a `const` of one. A schema is what a consumer validates a document
  against, and a document written before 0.14.0 is the same format at the
  same version - refusing it would have been the rename breaking every
  document ever written, through the one file whose job is to say what a
  valid document looks like.
- **Neither a case nor the audit schema pins `safe_command`'s command**
  (section 8.3). A case compares by the grants, not as a whole string,
  and `velaris.audit.1.schema.json`'s pattern is `^\S+ <file> --allow .+$`
  where it named one command. What that section defines is the grant
  list; the text before `--allow ` is the producer's own command name,
  which this document does not define. Comparing the string had required
  every implementation to be called what the reference was called - and
  the reference was called something else until 0.14.0, so 27 L1 cases
  read as a changed verdict across the rename when nothing about the
  grants had changed. A corpus published for an implementation in any
  language must not ask it to be named a particular thing.

- **The corpus keeps the names a published implementation opens**, and is
  the one part of this repository that is not renamed: `tests/index.json`
  keeps the `format` `velaris.conformance-corpus/1`, and the three schemas
  beside it keep their filenames - `schemas/velaris.audit.1.schema.json`,
  `velaris.capabilities.1.schema.json` and `velaris.capabilities.0.schema.json`. The corpus exists for an
  implementation in any language to run, and every implementation that
  exists today is a released version of the reference, each of which reads
  that field strictly and none of which can be changed. A corpus that
  said `sabline.conformance-corpus/1` would stop `velaris conformance`
  for everyone who has not upgraded - the break this rename is written to
  avoid. The reference reads both names from 8.6.0, and the name the
  corpus is written under moves no sooner than 0.15.0, when a reader that
  accepts both is the norm rather than the newest release. The same holds
  for the three schema files: a released implementation opens them by name
  (`conform.py`), so renaming them would have been the same break by
  another route. The reference looks for the `sabline.*` name first and
  falls back, so it is ready for the move before the move happens. The two
  predicate schemas, `capability-predicate.v1.schema.json` and
  `receipt-predicate.v1.schema.json`, are named for the types rather than
  the project and never carried either name.

An implementation that claims conformance to 0.13.0 conforms to 0.14.0
without changing anything it computes; what it must change is the name it
writes in a document's `schema` field and in a Statement's `predicateType`,
and what it accepts when reading is a superset of what it accepted before.

## 0.13.0 - Tools a host offers, and a MAC under a secret key - 2026-09-20

Tracks velaris-lang 8.5.0. Additive: a budget, an audit, a baseline and a
receipt that were valid under 0.12.0 are valid and mean the same.

- **A ninth effect, `tool`** (sections 3.1, 4.1 and the new 5.6): `tool`,
  `tool:T`, `tool:T:A=P`, `tool:T@N` and `tool@N`. Section 5.6 states how a
  pattern is matched - against the whole value, with `*` never standing for
  the literal that follows it, a separator, white space or a control - and
  that a held argument must be given.
- **`velaris.tools/1`**, a manifest of tools (the new section 8.10), is
  provisional. What travels between a run and its host is the reference's,
  and is not part of this format.
- **A MAC under a secret key** (section 8.6): `hmac_sha256` and
  `hmac_sha256_chain` are operations of `declassify`, and each call is an
  entry in the audit's `secrets.declassifications` with the reason `hmac
  signature` and a `builtin` key.
- **The audit** gains `tools`; `net_hosts`, and a baseline's grants (section
  9.3), name the host of a URL whose fixed beginning holds the `/` that ends
  the host. An audit of the same program is narrower than under 0.12.0,
  never wider.
- **A receipt** gains `grants_used` - what each grant let through, by the
  grant's own text - and `key_fingerprint`, `tool_calls` and `tool_ceiling`
  (section 8.7).
- The schemas take `tool` wherever an effect is named, `tool:T` as a
  baseline grant, and the receipt's and the audit's new fields.
- The corpus is unchanged at 456 cases: cases for `tool` join it when
  section 8.10 stops being provisional.
- The quoted reference text (section 2) is velaris-lang 8.5.0's.

## 0.12.0 - What the operating system held - 2026-09-19

Tracks velaris-lang 8.4.0, which asks the operating system to hold a run's
budget as well as enforcing it in the interpreter. **A receipt's
`run_parameters.confinement` is a level**: `full` when the operating system
held every file, network and process limit of the budget, `partial` when it
held some, `none` when the budget was the only boundary. Three optional
fields are added beside it within version 1: `confinement_reason`, each limit
that was not held and why; `confinement_layers`, the producer's names for the
mechanisms it applied; and `os_policy_sha256`, the digest of the policy the
producer derived from the budget. Until now `confinement` was `none`, or
under the reference's evaluation profile the name of a mechanism
(`landlock-net`, `landlock`, `job-one-process`, `sandbox-exec`); a receipt
written before 0.12.0 still validates and is read as it was written.

**`velaris.audit/1` gains `confinement`** within version 1 (section 8.2):
for a run under `safe_command`, the level and the reason on each of three
systems, and the granted Python modules that widen what is asked of the
operating system, each with what it widens it to. It is derived from the
budget alone and reads nothing of the producing machine, so an audit is
still the same bytes wherever it is made.

**Section 8.9**: a producer that writes the evaluation profile's name must
not have run the program at `none`. Appendix B lists the reference's E319,
which no program reaches. `schemas/receipt-predicate.v1.schema.json` and
`schemas/velaris.audit.1.schema.json` hold the new fields.

No rule of sections 3 to 7 or 9 changes and no conformance case changes.
Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word for
word.

## 0.11.0 - Names on a domain the project holds - 2026-09-15

Tracks velaris-lang 8.3.0. **The two predicate types are renamed**:
`https://velaris-lang.dev/capability/v1` (section 8.5) and
`https://velaris-lang.dev/receipt/v1` (section 8.7), on a domain the
reference's project holds. Until now they were named on the reference's
GitHub Pages address, under its maintainer's account name, which now
redirects to velaris-lang.dev. Every Statement and receipt written before
velaris-lang 8.3.0 names the earlier address, so each earlier name is
accepted for verification - a consumer reads it as the same type - and a
producer writes the new name. `velaris.dev` was never this format's domain;
it is registered to someone else, and it names no type defined here.
`schemas/capability-predicate.v1.schema.json` and
`schemas/receipt-predicate.v1.schema.json` name the new types, and
`tools/validate.py` accepts both names for the examples, which are the
Statements velaris-lang 4.2.0 and 8.1.0 wrote.

A receipt gains two optional fields within version 1: `run_parameters.profile`
and `stop`. **Section 8.8 is new**: what a receipt compared with an audit,
and with earlier receipts of the same subjects, can name as a difference,
and the shape of the reference's provisional `velaris.receipts-diff/1`.
**Section 8.9 is new**: what a receipt of a run under an evaluation profile
(`profile: "eval"`) asserts - no net, ffi or env, time and memory limits,
the receipt outside the budget, a stop honoured and recorded - the
confinement words the reference writes, and `stop`. Appendix B lists the
reference's E615 and E616.

No rule of sections 3 to 7 or 9 changes and no conformance case changes.
Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word for
word.

## 0.10.0 - A record of one run - 2026-09-14

Tracks velaris-lang 8.1.0. **Section 8.7 is new**: `velaris.receipt/1`, and
the in-toto predicate type
`https://gowrishankar-infra.github.io/velaris-lang/receipt/v1` that carries
it. Where the Statement of section 8.5 says what a program may do before it
runs, a receipt says what one run of it did: the budget it was given, each
refusal as its code, effect and line, each declassification with the reason
written in the program, the parameters it ran under (seed, frozen clock,
time and memory limits, and what operating-system confinement it had), how
it ended and how long it took. Its subjects are the files that ran, by the
same digests 8.5 uses, so an audit and a receipt of one program are matched
by digest.

A receipt MUST NOT hold a value the program handled - not its output,
input, arguments or environment, not a message quoting one, not the path or
host a refused operation named, not a declassified value. Section 8.7 also
says what it does not hide: a program's exit status, the lines it reached,
how many times it did something and how long it ran are in a receipt, and a
program that has declassified a value can choose them from it.

`schemas/receipt-predicate.v1.schema.json` is the predicate's schema;
`tools/check_sync.py` holds it to the copy velaris-lang publishes at the
type's URL, and `tools/validate.py` holds two receipts velaris-lang wrote
to it: `examples/run-receipt.json`, of `examples/effects.vel` with the
budget velaris-lang's release workflow grants it, and
`examples/refused-receipt.json`, of the same program given no `fs`, with
the one refusal that stopped it. Appendix B lists the reference's three
new codes: E515 (an import from outside the directory a program is served
from), E613 and E614 (a check or audit stopped at its time or memory
ceiling).

No rule of sections 3 to 7 or 9 changes and no conformance case changes.
Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and 7.1 word for
word.

## 0.9.0 - What ships as native code - 2026-09-14

Tracks velaris-lang 8.0.0. **No rule of this format changes.**
`velaris.audit/1` gains one field within version 1 (section 8.2, under
8.1's compatibility rule): **`ffi_native`**, per named Python module
whether native code - a compiled extension (`.so`/`.pyd`/`.dylib`) or a
module built into the interpreter - ships with it, decided from files on
disk **without importing** the module. Its value is `"native"` when one
is found and `"unknown"` otherwise; never `"false"`, because a
pure-Python module can import a native one without that showing in its
own files. It reflects the packages installed on the machine that
produced the audit, so it is not reproducible across machines, and an
attestation embedding it (section 8.5) says only what that machine
found. A producer without the notion writes it empty or omits it, and a
consumer ignores a field it does not know.

velaris-lang 8.0.0 is a major version, but its breaking changes are in
the reference's runtime and error codes - a proxy the `net` budget does
not cover is refused (E317), a function named like a built-in is refused
(E204), `read_file` of a documented credential location is refused
(E318), and `velaris add` refuses two redirects - not in this format.
Appendix B lists the three new codes as the reference's own, not part of
the static rule this document specifies. No conformance case changes;
the corpus is unchanged. Section 2 still quotes velaris-lang SPEC.md
sections 6, 7 and 7.1 word for word, so `tools/check_sync.py` still
passes.

## 0.8.0 - What the secrets section does not claim - 2026-09-12

Tracks velaris-lang 7.0.0, which closed a hole in the type 6.0.0
introduced, the same day 6.0.0 shipped. **No rule of this format
changes**: `declassify` is still the eighth effect of section 3.1,
`secrets` still holds the same three fields, and an implementation with
no such type system is unaffected. Two places here describe the change,
and both narrow a claim rather than making one.

**8.6.** The section said the rule behind `secrets` bounds explicit
flow only, and that a program with `declassifies: false` could still
tell a reader about a secret through its own control flow. That was
true of velaris-lang 6.0.0, where a comparison over a protected value
gave an ordinary boolean - and it was a hole, not a trade: with a
length and a character read, a comparison in a loop reads the whole
value out and the program prints it. 7.0.0 makes a comparison give
another protected value and refuses any branch on one, so the bullet is
narrowed to what remains true - that this is not a non-interference
result, and says nothing about how long a program runs, how much it
allocates, whether it stops, or what an operator learns by running it
repeatedly.

**Appendix B.** E563 joins E560, E561 and E562 as a compile-time code
the reference's type gives and this format does not require: an `if` or
`while` branching on a value derived from a protected one. E560 also
covers an operation that can fail, because a failure's reason is text
the program can print.

The corpus grows from 455 cases to 456. Two L1 audit cases are
reworded, because the programs they held branched on a protected value
or printed a boolean derived from one, and neither compiles now; and
one new L1 case records that refusal, `L1-audit-secret-branched-on`.

**Two defects in this repository's own tools, both from 0.7.**
`schemas/velaris.capabilities.1.schema.json` enumerates the effect
names twice - the grants a baseline may hold, and the effects a
function may declare - and 0.7 added `declassify` to neither, so a
baseline naming it was rejected as invalid. And `tools/validate.py`
parsed a grant by its prefix, with a fallthrough that read anything
unrecognised as a bare `net`: `declassify` was taken as a grant of
every host, so a baseline holding both reported every `net:` grant as
redundant. Both are fixed here, and the plain-effect list in the
validator is now one constant rather than two literals, so the next
effect cannot be added to one and not the other.

## 0.7.0 - An eighth effect, and what the audit says about secrets - 2026-09-12

Tracks velaris-lang 6.0.0, which added `Secret of T` - a value the
reference's type system will not let a program print, write, send or
pass to the host language. Two things follow for this format: one new
effect, and one new field. Nothing else changes: no grant form, no
refusal code, no parsing rule, no existing field.

**3.1, the effects.** `declassify` is the eighth, and it is different
from the other seven in what it covers: it reaches nothing outside the
program. It is an effect because the reference marks certain values as
ones a program may not emit, and `declassify` is the only operation
that removes the mark - so declaring it, propagating it through the
call graph and refusing it from a budget all matter, and all work
exactly as they do for the other seven. Nothing in sections 4 to 7
treats it specially: `declassify` is a grant like `io`, a denial like
`io`, and a name in `effects` like `io`. An implementation with no such
type system has no operation covered by it and a program written for
one never declares it; the effect is still in the grammar, so a budget
naming it parses everywhere.

**8.6, `secrets`.** `velaris.audit/1` gains an object saying which
builtins handed the program such a value (`sources`), whether it ever
declassifies one (`declassifies`), and with what stated reasons and in
which functions (`declassifications`). A consumer asks one question of
it - *does this program ever let a secret out* - and gets an answer
without running the program. It is an added field within version 1, so
a consumer that does not know it ignores it (8.1), and a producer with
no such type system writes empty values.

The section says what the field does not claim, because it would
otherwise be read as more than it is: the reasons are text a program's
author wrote and nothing checks them; the rule behind it bounds
explicit flow only, so a program with `declassifies: false` can still
tell a reader things about a secret through its own control flow; and
it covers only the values those builtins produced, not a secret that
arrives through standard input, the arguments, the network or the host
language.

**The corpus grows from 444 cases to 455.** Eight new L1 cases: the
`secrets` field for a program that holds a secret and never lets it
out, for one that declassifies, for one whose secret comes from a file,
and for one with no secret at all; and the four refusals around it - a
secret given to something that emits it, a signature that does not say
so returning one, a `declassify` whose reason is not written in the
call, and a `declassify` without the effect declared. Three new L2
cases: the `declassify` grant refused, the same grant allowed, and a
secret read and compared without any grant beyond `env`. One existing
L2 case, `L2-env-under-io`, is reworded: the program it held printed
what `env()` returned, which no longer compiles, so it now compares
instead - the case still tests what it always tested, that an `io`-only
budget refuses `env` at run time.

PRIOR_ART.md's TACIT entry said this format had no counterpart to
TACIT's information-flow control. That was true until velaris-lang
6.0.0; it now says what there is, and what TACIT still has that this
does not - capture checking over every value's type rather than one
wrapper type, and a stronger result than bounding explicit flow.
CaMeL's entry is corrected the same way.

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
