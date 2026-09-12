# Conformance

Version 0.6.0, 2026-09-12. What an implementation must do to claim that
it conforms to the Velaris capability format - `velaris.capabilities`
conformance - at each of three levels, and how it shows that it does.
Dedicated to the public domain under CC0 1.0, like the rest of this
repository.

The format is [SPEC.md](SPEC.md). This document names, for each level,
the behaviours of SPEC.md an implementation must have, and the cases of
the conformance corpus in [tests/](tests) that test them. The corpus is
the test; [tests/README.md](tests/README.md) is the contract for
running it. Where SPEC.md and the corpus disagree, that is a bug in one
of them, and until it is fixed the corpus decides.

## The levels

| Level | Name | For | Needs | Cases |
|---|---|---|---|---|
| L1 | Declaration | a tool that reads a program and says what it may do: a checker, an auditor, a reviewer | nothing else | 298 |
| L2 | Enforcement | a runtime that runs a program under an operator's budget | L1 | 37 |
| L3 | Ratchet | a check that holds a repository to its declared capability surface | L1 | 109 |

A claim at L2 or L3 is a claim at L1 too. L3 does not need L2: a tool
with no runtime at all can write and check baselines, and conform at L1
and L3.

## Proofs are not required

No level requires a theorem prover, or any proof of anything. An
implementation with no prover can conform fully, at all three levels.
Nothing in SPEC.md sections 3 to 9 depends on one, and no case's
expectation does: the corpus never compares the fields of
`velaris.audit/1` that record proofs (`functions[].status`,
`proven_share`), and the derivation of a baseline runs no prover
(SPEC.md 9.3).

The reference implementation, velaris-lang, goes beyond conformance.
It proves contracts with the Z3 prover before running, compiles proven
code to native, and has an HTTP door and an MCP server with ceilings, a
worker pool, SARIF output, `velaris review`, an invocation log and a
signed manifest of its tools. None of that is part of the format, and
none of it is needed to conform.

## L1 Declaration

An implementation conforming at L1 does all of the following.

- **D1. Parses the budget grammar**, as SPEC.md 4 and 5 define it:
  every form of 4.1; the algorithm of 4.2, including empty and quoted
  empty items, the `ffi:` continuation form, and counts of ASCII digits
  on `fs` and `net` only; additive grants and the smallest count (4.3);
  denials (4.4); `fs` directions and paths, and the percent-escapes of
  5.1; `net` hosts, ports, bracketed IPv6 addresses, escapes and
  one-label wildcards (5.2); `ffi` modules up to the first dot (5.3).
  Cases: the 51 `L1-budget-*` cases that parse, each compared with the
  grants it means.
- **D2. Refuses every malformed budget whole**, before any program
  runs, and never grants part of it (4.2). Cases: the 225
  `L1-budget-malformed-*` cases, and the refused `L1-budget-*` cases:
  a module after an effect in the continuation form, a raw comma in a
  path, a scoped denial, an unknown denial. A denial is tested against
  the grants the case writes (`L1-budget-deny-from-grants-given`);
  what a denial alone narrows is the runtime's default budget (4.6),
  which this document does not fix and no case tests.
- **D3. Checks declarations before running** (3.2): refuses a program
  that performs an effect it does not declare (T1), calls a function
  without declaring what it declares (T2), passes an effectful
  function as a value (T4), calls an effectful function in a contract
  (T5), or names anything but the seven effects in `uses`. Cases:
  `L1-audit-undeclared-effect`, `-declaration-propagates`,
  `-effectful-function-as-value`, `-effectful-call-in-contract`,
  `-unknown-effect-name`.
- **D4. Computes the effect surface from source** (3.2, 8.2): the
  effects of the audited file as the union of its functions'
  declarations; each function's declaration and whether it can fail;
  the literal paths, hosts and modules the program names, over every
  file it loads, and whether one is built while running (`read_any`,
  `write_any`, `any`, `ffi_any`). Cases: the 13 `L1-audit-*` cases
  that compile.
- **D5. Emits `velaris.audit/1`** (8) that validates against
  [schemas/velaris.audit.1.schema.json](schemas/velaris.audit.1.schema.json),
  whose `effects` holds only the seven names even when `ok` is false,
  and whose `safe_command` is derived as 8.3 says and always parses.
  Cases: all 18 `L1-audit-*` cases.

## L2 Enforcement

An implementation conforming at L2 conforms at L1, and does all of the
following for every operation of SPEC.md 3.1.

- **E1. Fixes the budget before the first statement** (6, G1).
- **E2. Checks each operation when it is attempted**, in the order of
  G2 - the effect (E310), then the scope (E311, E313, E314), then the
  count (E315) - and lets no refused operation happen: no file opened,
  no connection made, no module touched. Cases: every refused `L2-*`
  case, each with the code it must carry.
- **E3. Ends the run on a refusal**, which the program cannot catch
  and after which none of it runs (G3). Cases:
  `L2-refusal-cannot-be-caught`, and every refused case's
  `stdout_excludes`.
- **E4. Makes a redirect outside the grants a failure the program can
  handle**, naming the target, and follows one inside them (G4, 5.2).
  Cases: `L2-redirect-to-ungranted-host-is-a-failure`,
  `L2-redirect-to-granted-host-is-followed`.
- **E5. Checks what a run attempts, not what it declares** (G5), so an
  honest program runs under the budget it needs. Cases: the nine
  `L2-*` cases whose outcome is `completed`.
- **E6. Holds every escape route the reference's sandbox suite holds,
  that the corpus can state without a host language**:
  - an effect refused under `io`: reading, writing, the network,
    Python, a Python handle, the clock, randomness, the environment
    (`L2-read-under-io`, `-write-under-io`, `-net-under-io`,
    `-ffi-under-io`, `-ffi-handle-under-io`, `-clock-under-io`,
    `-rand-under-io`, `-env-under-io`);
  - an effect two helpers below `main` (`L2-effect-behind-two-helpers`);
  - denials, one and several, each against a budget the case grants
    (`L2-deny-one`, `L2-deny-several`);
  - a module outside `ffi:`, through `py`, a dotted module name,
    `py_json` and `py_new` (`L2-ffi-module-outside-list`,
    `-ffi-submodule-path`, `-ffi-through-py-json`,
    `-ffi-through-handle`);
  - a path outside the prefix, a write under a read grant, `..`, and a
    symbolic link (`L2-fs-read-outside-prefix`,
    `-fs-write-under-read-grant`, `-fs-dotdot-escape`,
    `-fs-symlink-escape`), and an existence check under a write grant,
    which is allowed (`L2-fs-exists-under-write-grant`);
  - a host not granted, a port not granted, a wildcard's parent domain,
    and a URL with no scheme, which is HTTPS at port 443
    (`L2-net-host-not-in-list`, `-net-port-not-in-list`,
    `-net-wildcard-parent-domain`, `-net-no-scheme-is-https`);
  - counts on `fs` and `net`, `@0`, and a count spent by an operation
    that then fails (`L2-fs-count-reached`, `-net-count-reached`,
    `-fs-count-zero`, `-fs-count-spent-by-failed-operation`);
  - additive `fs` and `net` grants (`L2-fs-additive`,
    `L2-net-additive`).
- **E7. Bounds an `ffi:M` grant to the module a call actually reaches**
  (5.3). This is required, but the corpus does not test it: every such
  case depends on the host language's object model, so the six in the
  reference's suite, written against Python, are left out and listed in
  `tests/index.json`. An implementation whose host language is Python
  can run them from velaris-lang's `check_sandbox.py`.

## L3 Ratchet

An implementation conforming at L3 conforms at L1, and does all of the
following.

- **R1. Writes `velaris.capabilities/1`** for a tree (9.2, 9.3, 9.4):
  every `.vel` file a program; its functions, effects, grants read from
  fixed text and reduced, and its `fs` and `net` counts; the surface as
  the union of the programs that compile; a file that does not compile
  recorded as such; a document that validates against
  [schemas/velaris.capabilities.1.schema.json](schemas/velaris.capabilities.1.schema.json).
  Cases: the 14 `L3-derive-*` cases, the 6 `L3-bound-*` cases and the
  3 `L3-reduce-*` cases.
- **R2. Does not replace a baseline unasked** (9.6): a writer asked to
  write again where a baseline exists, without being told in so many
  words to replace it, refuses. Case: `L3-write-writer-refuses-to-widen-unasked`.
- **R3. Compares with the baseline and nothing else** (9.1, 9.6): a
  widening fails at every later check until the baseline is edited,
  and a widening assembled over several changes is reported whole.
  Cases: `L3-sequence-gradual-widening`,
  `L3-sequence-merged-widening-keeps-failing`.
- **R4. Never passes when it cannot compare** (9.6): no baseline - so
  deleting it fails rather than turning the check off - a `/0`
  baseline, one that is not JSON, one holding a grant 9.2 does not
  allow. Cases: `L3-check-baseline-deleted`, `-baseline-provisional-v0`,
  `-baseline-not-json`, `-baseline-count-in-grant`.
- **R5. Applies the covering rule** (9.5) grant by grant. Cases: the 32
  `L3-covers-*` cases.
- **R6. Classifies widening and narrowing for every kind of scope**
  (9.6), reporting each widening's grant, count or function, program
  and rules W1 to W5:

  Every name in this table is a case id with `L3-check-` in front of
  it:

| Scope | Widens (fails) | Does not widen (passes) |
|---|---|---|
| an effect | `new-effect`, `stdlib-module-brings-net` | `narrowing`, `file-without-effects` |
| an `fs` path | `path-prefix-widened`, `new-direction`, `path-built-while-running`, `fs-declared-without-operation`, `declared-prefix-not-outside`, `backslash-climbs-out` | `declared-prefix-covers-under`, `another-spelling-of-a-path`, `literal-into-variable` |
| a `net` host | `url-built-while-running`, `url-star-is-any-host`, `declared-wildcard-not-parent`, `declared-port-not-portless`, `rules-named` | `declared-wildcard-covers-label`, `port-under-portless-grant`, `declared-port-covers-port` |
| an `ffi` module | `new-module`, `module-built-while-running` - a module named by a value built while running does not pass a baseline listing `ffi:math` | a module the baseline names: `known-limit-granted-module-behaviour` (R7) |
| a count | `count-raised`, `loop-without-fixed-turns`, `recursion-has-no-bound`, `version-never-hides-widening` | `loop-over-list-variable`, `statements-before-loop`, `narrowing` |
| a function | `function-gains-effect-grants-unchanged` (W5 alone), `import-widens-entry-not-surface` | `function-renamed`, `function-moved`, `reorder-and-reformat` |
| a program | `new-program-outside-surface` (W1), `entry-narrower-than-surface` (W3), `main-imported-from-outside`, `hidden-directory` | `new-program-inside-surface`, `stops-compiling` |
| the producer's version | - | `older-baseline-version`, `newer-baseline-version` |
- **R7. Matches the known limits as they are** (9.8). Five cases record
  what the reference does where the ratchet is known to be imperfect,
  and require the same:

| Case | Outcome recorded | Why it is imperfect |
|---|---|---|
| `L3-check-known-limit-rename-while-gaining` | pass | a function renamed in the change that gives it an effect its program already had is new to the baseline, so W5 does not see it; the declared surface did not widen |
| `L3-check-known-limit-granted-module-behaviour` | pass | a new call into a module the baseline already grants is inside the surface: a baseline records modules, not what they do |
| `L3-check-known-limit-bound-behind-call` | widened | a loop bound moved behind a function call has no bound the text fixes, so the count is null |
| `L3-check-known-limit-path-as-parameter` | widened | a path passed as a parameter is not fixed text, so the grant is unscoped, even when every caller passes a literal |
| `L3-check-known-limit-backslash-path` | widened | a path holding `\` is covered only by the same text (open question Q7), though on Windows it is inside the recorded prefix |

  The first two are widenings that pass; the last three are changes
  that do not widen and fail. The corpus records them so that another
  implementation matches the reference rather than guessing, and so
  that a change to any of them is a change to this repository, in
  review. What they mean for the claim a baseline makes is in SPEC.md
  9.8.

## Showing it

Run every case of the levels claimed, as [tests/README.md](tests/README.md)
says, and report each result. A claim is made in these words:

> *Implementation* *version* conforms to velaris-spec 0.6.0 at L1[, L2]
> [and L3], against the conformance corpus at velaris-spec commit
> *sha* (*n* cases), on *platform*. Not run: *case ids, and why*.

A claim holds only if no case of a claimed level failed. A case may be
left out of a claim only because the platform cannot meet its
`requires` - a symbolic link, or the reference's standard library -
and the claim names it. A case skipped for a missing tool, such as a
JSON Schema validator, leaves its level unshown.

velaris-lang's `velaris conformance [--level 1|2|3] [--json]` is the
reference's runner. It prints a line per level and a verdict, and
`--json` writes the report of tests/README.md. velaris-lang's CI runs
it on every leg, against this repository's corpus.

## What the corpus does not test

Required by SPEC.md, and not in the corpus:

- the attribute-chain bound of 5.3 (E7 above);
- 5.5, one budget inside another, which the reference uses for the
  ceilings of its doors and which a baseline check uses only through
  9.5;
- a URL with no host, or with a port that does not parse, refused with
  E314 even when `net` is unscoped (5.2);
- that a followed redirect spends no second count (5.2);
- the order of checks within G2 when two would refuse at once;
- G6, a runtime enforcing the budget for a program whose declarations
  it did not check.

Passing the corpus is evidence about the cases it holds, and no more.
The gaps are candidates for cases; a case that needs a host language
cannot be one.

## Where the corpus comes from

velaris-lang's `build_conformance.py` writes every case from a table in
one of that repository's suites - `check_sandbox.py`,
`check_library.py`, `check_ratchet.py` - where the same entry is
asserted against velaris-lang; it computes nothing itself. A drift test
in this repository's CI and in velaris-lang's regenerates the corpus
and fails when the result differs from what is committed, so the
corpus and the suites cannot say different things. A change to a case
is a change to a suite, made in velaris-lang, and a new version of this
repository.
