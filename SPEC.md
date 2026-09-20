# The Sabline capability format

Version 0.14.0, 2026-09-20. Dedicated to the public domain under CC0 1.0;
see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Reference implementation: sabline-lang,
<https://github.com/gowrishankar-infra/sabline-lang>. This text was
first extracted from sabline-lang 3.1.1 (commit `25d2c05`); version 0.2
tracked sabline-lang 3.3.0, which fixed the five defects the extraction
found; version 0.3 tracked sabline-lang 4.0.0, which reads and writes
the baseline of section 9; version 0.4 tracked sabline-lang 4.1.0,
and added a conformance corpus any implementation can run, in
[tests/](tests), with the levels of conformance in
[CONFORMANCE.md](CONFORMANCE.md); version 0.5 tracked sabline-lang
4.2.0, which writes the in-toto Statements of section 8.5; versions
0.5.1 and 0.5.2 tracked sabline-lang 4.2.1, and version 0.5.3 tracked
sabline-lang 4.3.2; none of the three changed a rule. Version 0.6.0
tracked sabline-lang 5.0.0, which made `io` the budget a run gets when
nobody writes one: sections 4.4 and 4.6 are restated, and one
conformance case that assumed the old default is replaced by one that
writes its grants down (section 10). Version 0.7.0 tracked sabline-lang
6.0.0, which added `Secret of T`: section 3.1 gains an eighth effect,
`declassify`, and section 8.6 is new - the `secrets` object of
`sabline.audit/1`, which says whether a program ever lets a secret out.
Version 0.8.0 tracks sabline-lang 7.0.0, which closed a hole in that
type the same day 6.0.0 shipped; no rule of this format changes, and
8.6 says more plainly what `declassifies: false` does and does not
claim. Version 0.9.0 tracked sabline-lang 8.0.0: `sabline.audit/1` gains
`ffi_native` (section 8.2), an added field within version 1 that says,
per named Python module, whether native code ships with it - found from
files on disk without importing the module. No rule of this format
changed; 8.0.0's breaking changes are in the reference's runtime and
error codes (Appendix B lists E204, E317 and E318), not in this format.
Version 0.10.0 tracks sabline-lang 8.1.0: section 8.7 is new -
`sabline.receipt/1`, a record of one run, and the in-toto predicate type
that carries it, bound to the same subjects as the Statement of section
8.5, so an audit and a receipt of one program are the before and the
after of the same bytes. No rule of sections 3 to 7 or 9 changes.
Version 0.11.0 tracks sabline-lang 8.3.0: both predicate types are named at
sabline.dev, a domain the reference's project holds, and each earlier
name is accepted for verification (sections 8.5 and 8.7); a receipt gains
`stop` and `run_parameters.profile` within version 1; and sections 8.8,
comparing receipts, and 8.9, a run under an evaluation profile, are new. No
rule of sections 3 to 7 or 9 changes.
Version 0.12.0 tracks sabline-lang 8.4.0, which asks the operating system to
hold a run's budget as well: a receipt's `run_parameters.confinement` is a
level - `full`, `partial` or `none` - with `confinement_reason`,
`confinement_layers` and `os_policy_sha256` beside it, and `sabline.audit/1`
gains `confinement`, both within version 1 (sections 8.2, 8.7 and 8.9). No
rule of sections 3 to 7 or 9 changes.
Version 0.14.0 tracks sabline-lang 8.6.0, which renames the reference
implementation from Velaris to Sabline and changes nothing else. The
document formats are `sabline.*` where they were `velaris.*`, and the two
predicate types are named at sabline.dev; every earlier name of each is
still read as the same thing (sections 8, 8.5 and 8.7). 0.13.0 tracked
sabline-lang 8.5.0, which added a ninth effect, `tool`
(sections 3.1, 4.1 and 5.6, and a manifest of tools in 8.10, which is
provisional); names the host of a URL that only begins fixed (sections 8.2
and 9.3); and, within version 1 of each document, adds `tools` to the audit
and an entry for a MAC under a secret key to its `secrets` (8.2, 8.6), and
`grants_used`, `key_fingerprint`, `tool_calls` and `tool_ceiling` to a
receipt (8.7). A budget, an audit, a baseline and a receipt that were valid
under 0.12.0 are valid and mean the same.
Conformance is defined by that corpus (section 10), not by this text.

## 0. About this document

This document specifies:

- the eight effects a Sabline program can declare, and the rule that
  makes a function's declaration cover everything a call to it can
  reach (section 3);
- the grammar an operator uses to grant effects, narrowed to paths,
  hosts, ports, Python modules and operation counts (sections 4 and 5);
- what a runtime enforcing a grant must refuse, and when (section 6),
  and what a grant does not bound (section 7);
- `sabline.audit/1`, the JSON report of what a program declares and
  names (section 8);
- `sabline.capabilities/1`, the JSON baseline in which a repository
  declares the capability surface its programs may have, and the
  comparison that fails a change which widens it (section 9);
- an in-toto predicate type that carries `sabline.audit/1` with the
  digests of the files audited (section 8.5);
- `sabline.receipt/1`, a record of one run of a program that holds none
  of the values it handled, and an in-toto predicate type that carries it
  with the digests of the files that ran (section 8.7).

It does not specify the rest of the Sabline language - types,
contracts, proofs, failure - or the time and memory limits a runtime
may also impose, or any command line or library interface beyond what
is needed to state the above. The reference implementation's own
SPEC.md, EMBEDDING.md and THREAT_MODEL.md cover those.

**Conventions.** MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be
read as described in RFC 2119 and RFC 8174 when, and only when, they
appear in capitals. "The reference" means sabline-lang 5.0.0. A
paragraph marked *Reference behaviour* records what the reference does
at a point this document does not yet settle; each such point is also
an open question in section 11. A paragraph marked *Resolved in 0.2*,
*0.3*, *0.4*, *0.5* or *0.6* records a point that an earlier version
left open, or stated wrongly, and that version settles, naming the
sabline-lang release that made the reference match.

Where this document and the reference disagree, that is a bug in one of
them. Until it is resolved, the conformance corpus decides (section
10).

## 1. Terms

| Term | Meaning |
|---|---|
| program | one or more `.vel` files: an entry file and what it imports |
| operator | whoever runs a program and chooses its budget |
| effect | one of the eight names in section 3.1 |
| declaration | a function's `uses` clause |
| budget | the grants an operator gives a run |
| grant | one item of a budget (section 4) |
| operation | one attempt by a running program to do something an effect covers - one file read, one request, one call into Python (section 3.1) |
| run | one execution of one program, from its start to its end |
| refusal | the runtime ending a run because an operation lies outside the budget (section 6) |
| producer, consumer | a program that writes, or reads, a document defined here |

## 2. The reference text

The three sections below are copied without change from sabline-lang
SPEC.md sections 6, 7 and 7.1 - the reference's own language
specification. They are the normative core of this document. Sections
3 to 7 state the same rules precisely enough to implement without
reading the reference's source, and say where the reference does
something this text does not.

`tools/check_sync.py` compares each block with sabline-lang SPEC.md and
fails if a word differs; this repository's CI runs it on every push and
every week. A change to those sections in sabline-lang is a change this
document must follow.

Section numbers inside the quoted text (such as "§8" and "§12") refer to
sabline-lang SPEC.md, not to this document.

### 2.1 Evaluation (sabline-lang SPEC.md section 6)

<!-- verbatim: sabline-lang SPEC.md "## 6. Evaluation" -->
Evaluation is strict, left to right, depth first. Arguments are fully
evaluated before a call. `and` and `or` short-circuit: the right side
is not evaluated when the left decides the result. `if`/`while`
conditions must be `Bool`; there is no truthiness.

There is no undefined behaviour. Every operation either produces a
value, raises a language error with a code, or fails in the sense of
§8.

<!-- end verbatim -->

### 2.2 Effects (sabline-lang SPEC.md section 7)

<!-- verbatim: sabline-lang SPEC.md "## 7. Effects" -->
A function declares what it may do:

    fn save(path: Text, body: Text) uses fs { ... }

The effects are `io` (the console: `print`, `read_line`, `args`),
`env` (environment variables, through `env()`), `fs` (files), `net`
(network), `clock` (the time), `rand` (randomness), `ffi` (calling the
host language, §12), `declassify` (turning a `Secret` into an
ordinary value, §3.1) and, from 8.5, `tool` (calling a tool the host
process offers, §7.2). `env` became its own effect in 3.0; before that
it was part of `io`, which meant an io-only budget could read every
secret in the environment. `declassify` became the eighth in 6.0: it
reaches nothing outside the program, but it is the one way a value the
type system protects stops being protected, and an operator has the
same reason to refuse it as to refuse `net`.

The rule is transitive and checked at compile time: a function may
only perform effects it declares, and calling a function requires
declaring everything that function declares. A function with no `uses`
clause is **pure** — it cannot perform any effect, and neither can
anything it calls, however deep. Violations are E300.

This is a property of the whole call graph, not a convention. Reading
a signature tells you the complete set of things a call can do to the
outside world.

<!-- end verbatim -->

### 2.3 The budget (sabline-lang SPEC.md section 7.1)

<!-- verbatim: sabline-lang SPEC.md "### 7.1 The budget" -->
Declaring an effect is the program's claim; the **budget** is the
operator's decision, given as `--allow` / `--deny` on the command line
or `allow=` in the library, and enforced by the runtime at the moment
an effect is attempted, whatever the source declares. A refusal stops
the program and cannot be caught.

An operator who writes no budget gets `io` - the console, and nothing
else. That is the default in 5.0 for `sabline file.vel`,
`sabline.run(source)` with no `allow`, `sabline.Pool(...)` with no
`allow`, and the ceilings of both doors. Before 5.0 the first three
granted all seven effects. `--deny` narrows whatever `--allow` gave,
so a denial alone narrows `io`; `--allow all` is a command-line
shorthand for every effect - the seven, and `declassify` from 6.0 -
written by the operator and never read from a caller's budget, and it
writes one line to standard error when it is used. `all` means all: an
operator who writes it has waived every gate, which is why writing it
is recorded.

A grant names an effect, and may narrow it:

| Grant | Permits |
|---|---|
| `io`, `env`, `clock`, `rand`, `declassify` | that effect |
| `fs` | any path, read and write |
| `fs:read`, `fs:write` | one direction, any path |
| `fs:read:P`, `fs:write:P` | one direction, for paths that resolve under `P` |
| `net` | any host |
| `net:H`, `net:H:PORT` | that host, at any port or at that port |
| `net:*.D` | hosts with exactly one label in place of the star |
| `ffi` | any Python module |
| `ffi:a,b` | those top-level modules |
| `tool` | any tool the host offers (8.5, §7.2) |
| `tool:NAME` | that tool |
| `tool:NAME:ARG=PATTERN` | that tool, with its argument `ARG` held to the pattern |
| `tool:NAME@N`, `tool@N` | at most N calls of that tool, or of tools, in the run |
| `...@N` | and at most N operations of that effect in the run |

Grants are additive. Paths are resolved with `realpath` when the budget
is parsed and again at every `read_file`, `write_file` and
`file_exists`, then compared as prefixes, so `..` and symlinks cannot
reach past a grant. A host is the URL's host name, lower-cased; a port
is the URL's port or the scheme's default; only `http` and `https` are
reachable. A wildcard matches one label and never the domain itself;
no wildcard may stand over an IP literal. A count is the smallest given
for that effect and counts every operation of that effect across the
whole run; a budget with no count is a budget on what, not on how much.

The refusals: E310 (the effect), E311 (a module outside `ffi:`), E313
(a path outside `fs:`, named), E314 (a host or port outside `net:`,
named), E315 (the count reached). One case is a catchable failure
rather than a refusal: a redirect whose target is outside the `net:`
grants fails the request, naming the target, because the program did
not choose where it was sent.

Outside the rule, and stated as such: a hard link inside a granted
directory is that directory's content; a file system changed by another
process between the check and the open is outside the model; where a
granted host name resolves is DNS's business.

<!-- end verbatim -->

## 3. Effects

### 3.1 The nine effects

| Effect | Covers | Operations in the reference (Appendix A) | Added |
|---|---|---|---|
| `io` | the console: standard output, standard error, standard input, the program's command-line arguments, its exit status | `print`, `log`, `ask`, `read_line`, `args`, `exit_with` | |
| `env` | reading environment variables | `env` | |
| `fs` | the file system: reading a file, writing a file, asking whether a path exists | `read_file` (read), `read_file_secret` (read, 6.0), `write_file` (write), `file_exists` (existence) | |
| `net` | the network: one HTTP or HTTPS request | `fetch`, `post`, `fetch_status`, `request` | |
| `clock` | reading the current time | `now` | |
| `rand` | drawing a random number | `random` | |
| `ffi` | calling into the host language - Python, in the reference - and using host objects | `py`, `py_int`, `py_float`, `py_json`, `py_new`, `py_do`, `py_field`, `py_close` | |
| `declassify` | turning a value the type system protects into an ordinary one | `declassify`; from 0.13, `hmac_sha256` and `hmac_sha256_chain` (section 8.6) | 0.7 |
| `tool` | calling a tool the process hosting the run offers | `tool`, `tool_secret` | 0.13 |

Effect names are lower case and matched exactly. The list is closed in
this version; a new effect is a new version of this document:
`declassify` is why there was a 0.7, and `tool` why there is a 0.13. The reference text's list for `io`
("`print`, `read_line`, `args`") names examples; the table above is the
complete list for the reference.

`declassify` differs from the other seven in what it covers: it reaches
nothing outside the program. It is an effect because the reference's
type system marks certain values as ones a program may not emit
(sabline-lang SPEC.md section 3.1, `Secret of T`), and `declassify` is
the only operation that removes the mark. Declaring it, propagating it
through the call graph and refusing it from a budget all work exactly
as they do for the other seven, and nothing in sections 4 to 7 treats
it specially. An implementation with no such type system has no
operation covered by `declassify`, and a program written for it never
declares one; the effect is still part of the grammar, so a budget
naming it parses everywhere.

`tool` differs in another way: what it reaches is not fixed by the
language. A tool is whatever the hosting process says it is, named in a
manifest the run is given (section 8.10). With no manifest there is no
tool, and an operation of the effect is refused even when the effect is
granted. An implementation that hosts no tools has no operation covered by
`tool`; the effect is still part of the grammar, so a budget naming it
parses everywhere.

Every other operation of the language is pure: it needs no effect and
is not checked against a budget. That includes reading JSON, all text
and number functions, and - in the reference - reading imported `.vel`
files while compiling (section 7).

### 3.2 Declarations, and what "transitive" means

A function declares effects with a `uses` clause naming zero or more of
them: `fn save(path: Text, body: Text) uses fs`. A declaration names
effects only. It cannot name a path, a host, a module or a count; those
exist only in budgets (section 4).

The static rule has five parts. A conforming checker MUST reject,
before running it, a program that breaks any of them:

- **T1.** A function may perform an operation only if it declares the
  effect that covers it (section 3.1).
- **T2.** A function may call another only if it declares every effect
  the callee declares - whether or not the callee ever performs them.
  Declarations propagate, not performances: a callee that declares
  `net` and does nothing still requires `net` of every caller.
- **T3.** A function with no `uses` clause is pure. By T1 and T2 it
  performs no operation, and neither does anything it calls, at any
  depth.
- **T4.** A function value - an inline function, or a named function
  passed as an argument - is pure. A function that declares any effect
  cannot be passed as a value. Calling a parameter that holds a
  function value therefore needs no effect.
- **T5.** A contract (`requires`, `ensures`, `invariant`) may call only
  pure functions.

*Transitive* means T1 and T2 together: one function's declaration is
the complete set of effects a call to it can perform, through any chain
of calls, including calls into imported files. It is a property of the
whole call graph and is checked without running the program.

What the rule does not say: which files, hosts or modules a function
reaches, or how many times. That is the budget's job. And the rule is
about what a program can attempt, not what it will: a declaration is an
upper bound.

The reference reports T1 and T2 as E300, T4 as E530, and T5 as E310 -
the same code as a runtime refusal (Appendix B), used here at compile
time.

A `uses` clause names effects, and the eight of section 3.1 are the
only ones. A conforming checker MUST reject a `uses` clause naming
anything else, before running the program, naming the effects it knows.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that the
reference accepted any identifier in a `uses` clause: `uses io, teleport`
compiled, `sabline.audit/1` listed `teleport` among the effects, and the
audit's `safe_command` became a budget that does not parse. From 3.3.0
the reference rejects an unknown name with E300, naming the seven. This
closes open question Q1.

*Resolved in 0.4 (sabline-lang 4.1.0).* Versions 0.2 and 0.3 concluded
from that rejection that `sabline.audit/1`'s `effects` is always a
subset of the seven. That was true of a document whose `ok` is true,
and not of the document that reports the E300: from 3.3.0 to 4.0.1 the
reference still listed `teleport` in that document's `effects`,
`functions[].effects` and `safe_command`, which then did not parse.
Writing the conformance corpus found it. From 4.1.0 an audit leaves a
name that is not an effect out of all three, whether or not `ok` is
true; the E300 problem still names it. A producer MUST NOT put any name
but an effect of section 3.1 in `effects` or `functions[].effects`.

## 4. The grant grammar

A budget is written as text: grants separated by commas, such as
`io,fs:read:./data,net:api.example.com:443@100`.

### 4.1 Forms

| Form | Grants |
|---|---|
| `io`, `env`, `clock`, `rand`, `declassify` | that effect |
| `ffi` | `ffi`, any module |
| `ffi:M` | `ffi`, for the module M only (section 5.3) |
| `fs` | `fs`, any path, both directions |
| `fs:read`, `fs:write` | `fs` in one direction, any path |
| `fs:read:P`, `fs:write:P` | `fs` in one direction, for paths that resolve to P or under it (section 5.1) |
| `net` | `net`, any host and port |
| `net:H` | `net` to the host H, any port |
| `net:H:PORT` | `net` to the host H at that port |
| `net:[A]`, `net:[A]:PORT` | `net` to the IPv6 address A, any port or that port |
| `net:*.D` | `net` to any host that is one label followed by `.D` (section 5.2) |
| `tool` | `tool`, any tool, any arguments (section 5.6) |
| `tool:T` | `tool`, for the tool named T, any arguments |
| `tool:T:A=P` | `tool`, for the tool T, with its argument A held to the pattern P |
| `tool@N`, `tool:T@N` | at most N calls of tools, or of the tool T, in the run; `tool@N` written with no tool named also grants every tool |
| an `fs` or `net` form followed by `@N` | the same, and at most N operations of that effect in the run (section 5.4) |

### 4.2 Parsing

The algorithm below is the definition of the grammar. Where it says
*error*, the whole budget is rejected before the program starts. An
implementation MUST NOT run a program under a budget it could not
parse, and MUST NOT drop an item it did not understand.

1. Split the text at every comma. Remove leading and trailing
   whitespace from each item.
2. Take the items from left to right. For each item:
   1. If it is empty, or exactly `''` or `""`, skip it. A budget with no
      items grants nothing. (The quoted forms exist because a budget
      handed to a child process in an argument list keeps the quotes a
      shell would have removed.)
   2. If it begins with `ffi:`, grant `ffi` and add the module named by
      the rest of the item to the named modules (section 5.3); the rest
      MUST be a module name, so `ffi:` with no module and `ffi:M@N` are
      errors (section 5.3). Then, while the next item is not empty,
      contains neither `:` nor `@`, and is not one of the effect names
      of section 3.1, add it as another module and move past it. So `ffi:math,json`
      names two modules; `ffi:math,io` names one module and grants `io`;
      `ffi:math,io,json` is an error, because `json` comes after `io`;
      `ffi:math,random` names the Python module `random`, while
      `ffi:math,rand` grants the effect `rand`. The named modules narrow
      `ffi` only while no plain `ffi` has been written; a plain `ffi`
      makes it every module (section 4.3).
   3. If it is `fs`, or begins with `fs:` or `fs@`, it is an `fs` grant
      (section 5.1).
   4. If it is `net`, or begins with `net:` or `net@`, it is a `net`
      grant (section 5.2).
   5. If it is `io`, `env`, `clock`, `rand` or `ffi`, grant that effect.
   6. Otherwise: error. Names are matched exactly, so `IO` is an error;
      and only `fs` and `net` take a count, so `io@5` and `ffi@5` are
      errors.
3. Counts. In an `fs` or `net` item, find the last `@`. If there is
   one, what follows it MUST be one or more of the digits 0 to 9, and
   is the count; sections 5.1 and 5.2 read the item without it. If what
   follows the last `@` is anything else: error.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that the
reference tested the count with Python's `str.isdigit`, which also
accepts other Unicode digits, so `fs@٣` was a count of 3 and `fs@²`
stopped the parser with an uncaught error instead of a budget error.
From 3.3.0 a count is the ASCII digits 0 to 9 only; every other form
after `@` is a budget error, and no malformed budget produces a
traceback. This closes part of open question Q6 (the other two parts,
`ffi:M@N` and `ffi:` with no module, are in section 5.3).

### 4.3 Combining grants

Within `fs` and within `net`, grants are additive. Two scoped items
grant both; an unscoped item (`fs`, `net`) makes the effect unscoped
whatever else is written, in either order. Counts combine by taking the
smallest (section 5.4), including a count written on an item whose
scope an unscoped item absorbed: `fs,fs:read:./a@5` is any path, at
most 5 operations.

`ffi` is additive too, the same way. A plain `ffi` grants every module;
an `ffi:M` item narrows `ffi` to the named modules only while no plain
`ffi` has been written. A plain `ffi` anywhere in the budget makes `ffi`
unscoped whatever else is written, in either order: `ffi,ffi:math` and
`ffi:math,ffi` both grant every module, because the wider grant wins,
exactly as it does for `fs` and `net`. Two `ffi:M` items grant both
modules.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded the reverse:
the reference restricted `ffi` to the named modules once any `ffi:M`
appeared, so `ffi,ffi:math` granted `math` alone, against the reference
text's "Grants are additive". Open question Q2 asked which of the two the
text should say. It is settled the additive way: from 3.3.0 the reference
makes the wider grant win, so the reference text and the parser now
agree, and `ffi` is additive like every other effect. This closes
open question Q2.

### 4.4 Denials

The reference also takes a list of effects to remove - `--deny net,ffi`
on its command line, `deny=` in its library - applied after the grants.
Each denied name MUST be one of the effects of section 3.1; it removes
the effect with its scope and count. A denial cannot be scoped:
`--deny fs:write` is an error.

When no grants are given, a denial narrows the runtime's default budget
(4.6), which this format does not fix. For the reference that is `io`
from sabline-lang 5.0, so `--deny net` alone leaves `io`; until 5.0 the
starting budget was all seven effects unscoped, so the same command
left five. A case in the conformance corpus therefore always writes the
grants a denial applies to.

### 4.5 A budget given as a list

Some interfaces take a budget as a list of strings. Each element SHOULD
be one complete item, and each module SHOULD be written as its own
`ffi:M`, because the continuation form of step 2.2 depends on order.
The reference library sorts the list and joins it with commas before
parsing, so `["ffi:math", "json", "io"]` becomes `ffi:math,io,json`, an
error; the reference HTTP door joins its list in no defined order.

### 4.6 When no budget is given

This format defines what a budget grants. It does not define what a
runtime does when the operator gives no budget at all. A tool built on
this format SHOULD require an explicit budget, or default to one that
grants no more than `io`.

From sabline-lang 5.0 the reference does the second everywhere: the
command line (`sabline file.vel`), the library (`sabline.run(source)`
with no `allow`), the worker pool (`sabline.Pool(...)` with no
`allow`), the MCP tool `sabline_run` and the HTTP `POST /run` all grant
`io` alone, and so do the two doors' ceilings. Until 5.0 the command
line, the library and the pool granted all seven effects, unscoped,
and this section recorded that; the two doors were narrowed earlier
(the MCP server in 3.4, the HTTP door in 4.0). The reference's command
line takes `--allow all` as a shorthand for the seven effects, written
only by the operator and never read from a caller's budget, and writes
one line to its standard error when it is used.

What makes a run deny-by-default is the budget, not the program or the
format.

The reference's two doors also have a ceiling, the most a request may
ask for, compared under section 5.5. For the MCP server it is `io`
unless its operator names a wider one (from sabline-lang 3.4); for the
HTTP door it is `io` from sabline-lang 4.0, where before a door started
without one granted all seven effects. A tool that takes budgets from
callers SHOULD have a ceiling, and SHOULD make it no wider than `io`
unless its operator says otherwise.

### 4.7 Canonical text

Informative. The reference writes a parsed budget back as text - to
hand it to a child process - as follows: the granted effects in sorted
order; `ffi` as `ffi`, or as one `ffi:M` per module in sorted order;
`fs` as `fs`, or as one `fs:D` or `fs:D:P` per grant in the order
written, with P resolved (section 5.1); `net` as `net`, or one `net:H`
or `net:H:PORT` per grant in the order written, IPv6 hosts in brackets;
an effect's count appended to every item of that effect; items joined
with commas; an empty budget as `''`. Resolved paths make this text
specific to the machine and directory it was written on.

## 5. Scoped grants

### 5.1 fs: directions and paths

An `fs` item, with its count removed, is `fs`, `fs:D` or `fs:D:P`. D
MUST be `read` or `write`; anything else after `fs:` is an error. P is
everything after the second colon, so on Windows `fs:read:C:\data` has
P = `C:\data`. If there is a second colon, P MUST NOT be empty.

A path whose last `@` is followed only by ASCII digits is read as a
count: `fs:read:./x@2` is `./x` with a count of 2.

**Escaping (0.2).** A path may hold any character, including a comma, an
`@`, a bracket or a percent sign, by writing these five percent-encoded:
`,` as `%2C`, `@` as `%40`, `[` as `%5B`, `]` as `%5D`, and `%` as
`%25`. The encoded forms carry none of the characters the grammar uses
as structure, so `%2C` survives the comma split of step 1 and `%40`
survives the count's `@`. When the budget is parsed, exactly these five
sequences are decoded, in one left-to-right pass, before the path is
resolved; every other `%` is literal, so a literal `%2C` in a path is
written `%252C`. `fs:read:./a%2Cb.txt` is the path `./a,b.txt`, and
`fs:read:./mail%40host` is `./mail@host`. This is the rule the
reference's `safe_command` (section 8.3) uses to write a path back, so a
path with a comma or an `@` round-trips.

**Resolution.** P is resolved when the budget is parsed. Every path an
operation names is resolved when the operation is attempted. Both use
the same function R:

1. make the path absolute against the process's current working
   directory at that moment;
2. resolve every symbolic link among its components that exist, and
   remove `.` and `..` components; components that do not exist are
   kept as written (the reference uses Python's `os.path.realpath`);
3. on Windows, lower-case the result and use `\` as the separator (the
   reference uses `os.path.normcase`); elsewhere, leave it unchanged.

A grant (D, P) permits an operation in direction d on the path Q when
D = d and R(Q) either equals R(P) or begins with R(P) followed by the
platform's path separator; a trailing separator on R(P) is ignored for
this comparison. The comparison is by whole components:
`fs:read:./data` does not permit `./database`. R(P) may be a file, and
then only that file is permitted. `fs:read` and `fs:write` permit every
path in their direction; `fs` permits every path in both.

The direction of each operation: reading a file is `read`; writing a
file is `write`; asking whether a path exists is permitted by either a
`read` or a `write` grant. The operation then acts on R(Q), the
resolved path, not on the text the program gave.

Because P is resolved at parse time, a grant is to what P named then.
If `./data` is a symbolic link when the budget is parsed, the grant is
to its target. A relative P names different directories when the same
budget text is parsed in different working directories.

### 5.2 net: hosts, ports and wildcards

A `net` item, with its count removed, is `net` or `net:S`. S is read as
a host and an optional port:

1. If S begins with `[`, the host is the text up to the next `]` (error
   if there is none, or if the brackets hold nothing), and after the `]`
   there MUST be nothing, or `:` followed by ASCII digits (the port).
   This is the form for an IPv6 address: `net:[::1]`, `net:[::1]:443`.
2. Otherwise, if S contains `:` and everything after the last `:` is
   ASCII digits, the host is the text before it and the digits are the
   port. Otherwise the whole of S is the host. In this form a host that
   is empty, or contains `/`, `@` or a residual `:`, is an error.
3. A port MUST be from 1 to 65535.
4. The host is lower-cased, and trailing dots are removed.

An IPv6 address MUST therefore be written in brackets, so that
`host:port` is never ambiguous. A residual `:` in an unbracketed host
(step 2) is an error, not a host name.

**Escaping (0.2).** A host may hold a `,`, `@`, `[`, `]` or `%` by
writing it percent-encoded, exactly as a path does (section 5.1): `,` as
`%2C`, `@` as `%40`, `[` as `%5B`, `]` as `%5D`, `%` as `%25`. The
structural read above is done on the encoded text - so `@` and `/` are
still errors as raw characters - and the host is decoded afterward. An
IPv6 zone identifier's `%` is therefore written `%25`: `net:[fe80::1%25eth0]`.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that the
reference read `net:::1` as the host `:` at port 1 and `net:h:x` as the
host `h:x`. From 3.3.0 an unbracketed IPv6 address is a budget error
naming the bracket form to use, and a host with a residual `:` is an
error, so `net:::1` no longer parses as a different host. This closes
open question Q5 for the grammar; section 8.4 closes it for
`safe_command`.

**Wildcards.** A host beginning with `*.` is a wildcard over the rest,
T. T MUST NOT be empty, MUST NOT contain `*`, MUST contain at least one
`.` (so `net:*.com` is an error), and MUST NOT consist only of labels
that are all digits (no wildcard over an IP literal). A `*` anywhere
else in a host is an error. The wildcard `*.T` matches a host h exactly
when h is L followed by `.` and T, where L is not empty and contains no
`.`: `*.example.com` matches `api.example.com`, and matches neither
`example.com` nor `a.b.example.com`.

**From a URL to a host and port.** When an operation names a URL U:

1. if U does not begin with exactly `http://` or `https://`, `https://`
   is put in front of it - `api.example.com/x` is an HTTPS request, to
   port 443;
2. U is split as a URL (RFC 3986; the reference uses Python's
   `urllib.parse.urlsplit`). The host is its host name, lower-cased,
   trailing dots removed, IPv6 without brackets. The port is the port
   the URL writes, or 443 for `https` and 80 for `http`;
3. a URL with no host, or with a port that does not parse, is refused
   with E314 - even when `net` is unscoped.

A grant (H, p) permits (host, port) when H matches the host - equal
text, or a wildcard match as above - and p is absent or equal to the
port. Matching is on text alone. No name is resolved to an address to
be compared, and no address is put in a canonical form: a grant for a
name does not permit its address, or the reverse; `127.0.0.1` and
`127.1` are different hosts; an internationalised name is compared in
whatever form the URL gives it.

**Redirects.** When a request is redirected, the target is checked
against the same grants, and against the rule that only `http` and
`https` are reachable, before it is followed. A target outside them
does not refuse the run: the operation fails with a failure the program
can handle, naming the target (G4 in section 6). A followed redirect is
part of the one operation already counted.

### 5.3 ffi: modules

`ffi:M` grants the module M, where M is the text after `ffi:` up to its
first `.`. `ffi:os.path` grants `os`, all of it. The same cut applies
to the continuation items of step 2.2.

When a program calls into the host language naming a module X - the
first argument of `py`, `py_int`, `py_float`, `py_json` and `py_new` in
the reference - the call names X and then a dotted path of attributes
reached from it (the function argument). An `ffi:M` grant bounds the
**whole path a call reaches**, not only the module X it names:

- The module X is checked first: the call is permitted when `ffi` is
  unscoped, or when the text of X up to its first `.` is one of the
  granted modules. The check happens before the module is imported.
- The attribute chain is then resolved step by step, and at each step
  the object reached is placed: a module by its own name, any other code
  object (a class, a function, a bound method) by the module its code
  lives in. If that top-level package is outside the grants, the call is
  refused with E311 naming the module actually reached. If it cannot be
  determined, the call is refused rather than allowed.
- Inert data - a number, text, bytes, a list, a map - is not code from
  any module and is not checked, so a legitimate deep attribute inside a
  granted module (`json.decoder.JSONDecoder`) still works.
- The same check applies to a method or attribute reached through a held
  object (`py_do`, `py_field`), and to a non-serialisable result kept as
  a handle: a handle to a granted module's object is not a door into an
  ungranted one.

So `ffi:M` bounds the modules a call may reach along the path it names.
It still does not bound what a *granted* module can do: `ffi:builtins`
grants Python's `open`; `ffi:subprocess` grants a shell; `ffi:os` is the
whole operating system. A granted module's own C-level re-exports count
as the module their code lives in, not as the module that re-exports
them: `os.system` is code in the `nt`/`posix` module, so it is reached
under `ffi:os,nt` (or `ffi:os,posix`), not under `ffi:os` alone.

`ffi` takes no count, and `ffi:` needs a module name.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that the
check covered only the module name X: the attribute chain was not
checked, so anything reachable by attribute access from a granted module
- including other modules it imported - was reachable, and
`py("json", "codecs.encode", ...)` ran `codecs` code under `ffi:json`.
From 3.3.0 the whole reached path is checked as above. This closes the
dotted-path part of open question Q9. Version 0.1 also recorded that
`ffi:math@5` was accepted as a module literally named `math@5` and
`ffi:` alone granted a module whose name is empty; from 3.3.0 both are
budget errors, closing the rest of open question Q6.

### 5.4 Counts

Only `fs` and `net` take counts. For each of the two, the run's limit
is the smallest count written on any item of that effect, scoped or
unscoped. With no count, there is no limit.

Every `fs` operation - read, write or existence check - spends one from
the run's `fs` count, and every request spends one from the `net`
count, whatever path or host it names. The count is spent after the
scope check passes and before the operation is attempted, so an
operation that then fails (a file that is not there, a host that does
not answer) has still spent one. An operation that would be the
(N+1)th of its effect in the run is refused with E315 and does not
happen. So at most N operations of that effect happen in a run, and
`@0` grants the effect while permitting no operation of it.

A count belongs to one run. A runtime that runs several programs in one
process MUST start each program's counts at zero; the reference's
worker pool installs the budget again before every program.

A count bounds how many operations there are - not their size, their
rate, or what they carry.

### 5.6 tool: names, argument patterns and counts

*New in 0.13.0 (sabline-lang 8.5.0).*

A tool's name T and an argument's name A are ASCII letters, digits, `_`,
`.` and `-`, beginning with a letter or `_`. A is a top-level key of the
call's arguments, which are one JSON object.

**Combining.** `tool` anywhere in the budget grants every tool with any
arguments, and scoped items then add nothing, as with `fs` and `net`
(section 4.3). `tool:T` anywhere grants T with any arguments, and patterns
written for T then add nothing: the wider grant wins. Otherwise T is granted
with each argument that has patterns held to them: patterns for one
argument are alternatives, and every argument that has any must match one.
An argument with no pattern is not held by the budget. A tool no item names
is not granted.

**Matching.** A pattern is matched against the whole value, as written:
nothing is trimmed, case-folded or normalised. Every character of the
pattern but `*` matches itself. `*` matches one or more characters, none of
which is: the character that follows the star in the pattern, if any; one
of `,` `;` `<` `>` `"` `'` `\`; white space; or a character of Unicode
general category C (controls, format characters) or Z (separators). A value
that holds `..` matches only a pattern that holds `..`. A value longer than
4,096 characters matches nothing. `**` is not a pattern. So `*@corp.com`
matches `ann@corp.com` and none of `ann@corp.com.evil.example`,
`eve@evil.example, ann@corp.com`, `eve@evil.example@corp.com` or
`Ann@Corp.com`.

A text value is matched as it is; a number as its JSON text; a boolean as
`true` or `false`. A list matches when it is not empty and every item
matches. An object, a null, and an argument that is not given do not match:
a held argument MUST be given, because a default the host would fill in is
not held to the operator's pattern.

**Writing a pattern in a budget.** `,` and `%` are written `%2C` and `%25`.
A count is a trailing `@` followed by ASCII digits and nothing else, so a
pattern may hold an `@` of its own; a pattern that ends in `@` and digits
writes that `@` as `%40`. A count goes on the tool (`tool:T@N`), not on an
item that holds an argument.

**Counts.** `tool:T@N` permits at most N calls of T in the run and `tool@N`
at most N calls of tools; the smallest count written for each applies. A
call is counted after the grants pass and before the host is asked, so a
call the host then fails has still spent one. The call that would be the
(N+1)th is refused and the host does not hear of it.

**Refusals.** A call of a tool that is not granted, or with a held argument
that does not match, is refused (E321 in the reference); past a count, E322.
Like every refusal it ends the run and the program cannot handle it.

**Covering (section 5.5).** A ceiling that grants `tool` with no count
covers any tool grants. Otherwise each item asked for MUST be written in
the ceiling, as canonical text: patterns are not compared for inclusion.

### 5.5 One budget inside another

The reference uses this relation for the ceilings of its HTTP door and
its MCP server (`--max-allow`): a request may ask for any budget the
ceiling covers. Section 9 uses it, grant by grant, for baselines. A budget C covers a
budget A when all of the following hold:

1. C grants every effect A grants.
2. If A grants `ffi` and C restricts `ffi` to modules, A restricts it
   too, and A's modules are a subset of C's.
3. If A grants `fs`: when C has an `fs` count, A has one no larger.
   When C's `fs` is scoped, A's is scoped too, and every grant (d, p) of
   A has a grant (d', q) in C with d' = d and either q absent, or p
   present and R(p) equal to R(q) or under it (section 5.1).
4. If A grants `net`: the same rule for counts. When C's `net` is
   scoped, A's is scoped too, and every grant (h, p) of A has a grant
   (H, P) in C with P absent or equal to p, and either H and h are both
   wildcards and equal, or h is not a wildcard and H matches it
   (section 5.2).

What follows from this: a scoped ceiling never covers an unscoped
request (`fs:read,fs:write` does not cover `fs`); a grant with a port
does not cover one without; a wildcard covers the same wildcard and
single hosts under it, not a narrower wildcard (`*.example.com` does
not cover `*.b.example.com`).

## 6. What the budget guarantees at runtime

A runtime that claims conformance MUST provide all of the following,
for every operation in section 3.1.

- **G1. The budget is fixed first.** It is in place before the
  program's first statement runs, and no operation of this format can
  change it. (A granted `ffi` module is outside this guarantee; see
  section 7.)
- **G2. Every operation is checked when it is attempted, in this
  order,** before it has any effect outside the program:
  1. the effect - not granted: E310;
  2. the scope - a module outside the `ffi:` grants: E311; a path
     outside the `fs:` grants: E313; a host or port outside the `net:`
     grants: E314;
  3. the count, for `fs` and `net` - exhausted: E315;
  4. then, and only then, the operation.

  No file is opened, no connection is made and no module is imported
  for an operation that is refused.
- **G3. A refusal ends the run.** It is not a failure value: the
  program's `check` does not see it, `try` does not pass it up, and no
  statement of the program runs after it. The run ends reporting the
  refusal's code and what was refused.
- **G4. One exception.** A redirect to a target outside the grants
  (section 5.2) is not a refusal. The program did not choose the
  target, so the operation fails with a failure the program can handle,
  naming the target, and the run continues.
- **G5. The budget is checked against what a run attempts, not against
  what it declares.** A program that declares `net` and never makes a
  request runs under a budget without `net`. A program that declares
  nothing runs under any budget and attempts no operation.
- **G6. Neither check depends on the other.** Declarations are checked
  before running (section 3.2); the budget while running. A runtime
  MUST enforce the budget even for a program whose declarations it did
  not check.

## 7. What the budget does not guarantee

Taken from the reference's THREAT_MODEL.md, and narrowed where this
format can say more exactly what it does not cover.

- **It is not a security boundary.** In the reference the budget is
  enforced by an interpreter written in Python, in the same process as
  the compiler and - unless a time or memory limit is set - the same
  process the program runs in. It guards against a program doing what
  it was not asked to. It belongs inside an operating-system sandbox, a
  network policy or a separate account when the stakes warrant one.
- **Anything a granted `ffi` module can do** (section 5.3). Files,
  network access, processes and environment reached through a granted
  module are not `fs`, `net` or `env` operations and are not checked
  against those grants. A grant of `ffi:os` is the whole operating
  system as the current user. From sabline-lang 3.3.0 an `ffi:M` grant
  is bounded to the module a call actually reaches along its attribute
  chain, so a granted module is not a door into the other modules it
  imported; but within a granted module, that module's full behaviour is
  granted.
- **What a granted path contains.** A hard link inside a granted
  directory is that directory's content. A file system changed by
  another process between the check and the open is outside the model.
- **Where a granted host name resolves, what a granted host does with
  what it receives, and the method, headers, size or content of a
  request.** A count bounds how many requests are made, not how much
  they carry or how fast they are made.
- **The console.** Command-line arguments and standard input are part
  of `io`, and so is anything written to standard output or error, in
  any quantity. The format says nothing about the meaning of what a
  program prints.
- **Existence under a write grant.** An existence check is permitted by
  a `write` grant alone, so a write-only grant lets a program learn
  whether paths under it exist.
- **Time, memory and processor use.** The reference offers a time limit
  and a memory cap as settings of a run, and from sabline-lang 4.0 its
  doors hold both to ceilings the operator sets. They are not part of
  this format, and they have platform limits of their own (see the
  reference's THREAT_MODEL.md).
- **Side channels**: timing, load, cache effects.
- **Reads while compiling.** In the reference, `import "path.vel"`
  reads source files during compilation; that is not an `fs`
  operation.
- **Logic errors, and code written in any other language.** The
  guarantees apply to what the enforcing runtime runs.
- **A defective or altered runtime.** Every guarantee here is a
  guarantee of the implementation that makes it.
- **A run given no budget** (section 4.6).

## 8. sabline.audit/1

`sabline.audit/1` is a JSON object that describes a program before it
runs: what it declares, what it names, what it promises, and whether
each promise is proven. In the reference it is what
`sabline.audit(source).as_dict()` returns, and what the reference's MCP
tool `sabline_audit`, the `POST /audit` endpoint of its HTTP door, its
npm `audit()`, its CrewAI audit tool, its GitHub Action's pull request
comment, and - from sabline-lang 3.3.0 - its command line's
`audit --json` are built on; from 4.2.0 it is also the predicate of the
in-toto Statements `sabline attest` writes (section 8.5). Its JSON
Schema is
[schemas/velaris.audit.1.schema.json](schemas/velaris.audit.1.schema.json);
[examples/audits/](examples/audits) holds four documents the reference
produced.

*Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that the
command line was the exception: in sabline-lang 3.1.1 `sabline audit
FILE --json` printed an older, unversioned summary with different fields
- `file`, `compiles`, `errors`, `effects`, `functions` as a count,
`proven`, `checked_at_runtime`, `reaching_outside`, `can_fail`,
`loops_unshown` as an object, `contract_coverage`, and a `safe_command`
built from the coarse effects alone - which the schema rejected because
it has no `schema` field. From 3.3.0 the command line prints
`sabline.audit(source).as_dict()`, the same document as every other
door, and its `safe_command` is derived as section 8.3 says (so
`examples/json_ffi.vel` gives `ffi:math,io`, not `ffi,io`). This closes
open question Q3.

### 8.1 Compatibility

Within version 1, fields may be added. No field changes meaning or
disappears without the `schema` value changing. A consumer MUST ignore
fields it does not know. Fields added after version 1 was first
released (in sabline-lang 2.52) are optional in the schema, because
documents from earlier producers lack them; the table says when each
was added.

### 8.2 Fields

| Field | Type | Meaning | Added |
|---|---|---|---|
| `schema` | string | `"sabline.audit/1"` | |
| `sabline_version` | string | the version of the producer | |
| `ok` | boolean | true when the program compiled: it parsed, and the checks the reference makes before running - of `main`, effects, types and proofs - reported no problem. A file with no `main` is audited as a library and is not a problem. A proof that a promise is false (E700) makes `ok` false. | |
| `problems` | array | one object per problem: `code` (`E` and three digits), `message`, `line` (integer), `file`, `fixes` (array of strings). Empty when `ok` is true. | |
| `effects` | array of strings | the union of the declarations of every function defined in the audited file, sorted, without repeats. Through the transitive rule it includes everything those functions can reach in imported files. When `ok` is true, it is an upper bound on the effects a run can attempt. When `ok` is false it is whatever could be read - not a bound - and may be empty. Either way it holds only names of the seven effects: a name in a `uses` clause that is not an effect is left out (section 3.2, resolved in 0.4). | |
| `functions` | array | one object per function defined in the audited file, in source order (inline function values are not listed): `name`; `effects`, its own declaration, sorted; `can_fail`, true when declared `or fail`; `requires` and `ensures`, each contract expression as text; `status`; `loops_unshown` (integer, added 2.62). | |
| `functions[].status` | string | `"proven"`: every promise was proven before running, which happens only when a prover ran. `"checked at runtime"`: it has promises, not all proven. `"no promises"`: no `requires` or `ensures`. `"error"`: a problem was reported on the function's line. | |
| `proven_share` | number or null | 100 × (functions with a promise whose status is `"proven"`) ÷ (functions with at least one `requires` or `ensures`), rounded to one decimal place; null when no function has one | |
| `safe_command` | string | `sabline <file> --allow G`, where `<file>` is literal text for the reader to replace, and G is the grant text of section 8.3, or `''` when that is empty | |
| `warnings` | array of strings | sentences for a human reader. Their wording is not part of the format and a consumer MUST NOT parse it. | |
| `ffi_modules` | array of strings | sorted names, each the text up to its first `.`, of every module given as literal text in the module argument of `py`, `py_int`, `py_float`, `py_json` or `py_new`, anywhere in the program as loaded - the audited file and every file it imports | 2.60 |
| `loops_unshown` | integer | loops in the audited file whose termination the reference's rule (sabline-lang SPEC.md section 9.5) does not show, including loops inside inline function values | 2.62 |
| `contract_coverage` | array of strings | functions in the audited file that take or return a `List`, a `Map` or a record and have no `requires` or `ensures` | 2.62 |
| `fs_paths` | object | `read` and `write`: sorted arrays of path text, exactly as written, not resolved. `read` holds the literal first argument of every `read_file` and `file_exists` call anywhere in the program as loaded; `write`, of every `write_file` call. `read_any` and `write_any`: true when some such call's argument is not a literal. | 3.0 |
| `net_hosts` | object | `hosts`: a sorted array. For each literal URL given as the first argument of `fetch`, `post` or `fetch_status`, or the second of `request`, anywhere in the program as loaded: `https://` is put in front if it begins with neither `http://` nor `https://`; the host is lower-cased and trailing dots removed; the entry is the host, or `host:port` when the URL writes a port. From sabline-lang 3.3.0 an IPv6 host is written in brackets (`[::1]`, `[::1]:443`), so `host:port` is never ambiguous, and any of `, @ [ ] %` in a host is percent-encoded (a `net:` grant, section 5.2). `any`: true when some such argument is not a literal, or has no host. | 3.0 (IPv6 bracketed, 3.3) |
| `ffi_any` | boolean | true when the module argument of some `py`, `py_int`, `py_float`, `py_json` or `py_new` call, anywhere in the program as loaded, is not a literal - a module named by a value built while running, which `ffi_modules` cannot list | 4.0 |
| `counts` | object or null | `fs` and `net`: for each, the largest bound of section 9.4 on the operations of that effect one call to a function defined in the audited file can perform (`0` when none of them declares the effect), or `null` when the text fixes no bound or the bound exceeds 2^53. For a file whose `main` calls every other function, a bound on one run. The whole field is `null` when no bound was determined, as when `ok` is false. | 4.2 |
| `prover` | boolean | true when a prover decided the `status` of the promises: one was present and the program compiled. False otherwise - no prover, or `ok` false - and then no `status` is `"proven"` and a `proven_share` of 0 says nothing about what a prover would prove. | 4.2 |
| `secrets` | object or null | which builtins handed the program a value the type system will not let it emit, whether the program declassifies one, and with what reasons (section 8.6). `null` when the program could not be loaded. | 0.7 |
| `ffi_native` | object | per top-level Python module the program names (keys are a subset of `ffi_modules`), whether it or code it ships is native - a compiled extension (`.so`/`.pyd`/`.dylib`) or built into the interpreter - decided from files on disk **without importing** the module: `"native"` when one is found, `"unknown"` otherwise and never `"false"`, since a pure-Python module can import a native one without that showing in its own files. It reflects the packages installed on the producing machine, so it is not reproducible across machines. Empty when no module is named. | 0.9 |
| `tools` | object or null | `names`: sorted, without repeats, the tool named as literal text in the first argument of every `tool` or `tool_secret` call anywhere in the program as loaded; `any`: true when some such call names its tool with a value built while running. `null` when the program could not be loaded | 0.13 |
| `confinement` | object or null | what the operating system holds of a run under `safe_command`, beside the budget (section 8.7, `run_parameters.confinement`): `systems`, an object whose keys are `linux`, `macos` and `windows` and whose values each have `level` - `"full"`, `"partial"` or `"none"` - and `reason`, text saying what is not held and why, stated for a system where every mechanism the producer uses there is available; and `widened_by`, an array of `{"module", "widens", "known"}`, one for each granted Python module that widens what the producer asks of the operating system - `widens` holds `"fs"` (any path), `"net"` (any host) or `"all"` (nothing enforced), and `known` is false for a module the producer has no entry for, which it treats as `"all"`. It is derived from the budget alone and reads nothing of the producing machine, so it is reproducible across machines; what one run actually got is in that run's receipt. `null` when `safe_command`'s budget does not parse, and absent from a producer that asks nothing of the operating system. | 0.12 |

Two scopes are at work, and they differ. `effects`, `functions`,
`loops_unshown`, `contract_coverage` and `counts` describe the functions
defined in the audited file. `ffi_modules`, `ffi_any`, `fs_paths` and
`net_hosts` read the literals of every function loaded, including
functions in imported files that the program never calls, so they can
list more than the program's own calls reach.

**A URL that begins fixed** *(0.13.0)*. For `net_hosts`, a URL argument
names its host when it is a literal, as before, and also when only its
beginning is fixed: `+` whose leading operands are literals, or `format`
whose template is a literal, read up to its first `{}`. The fixed beginning
names the host only when it matches `http://` or `https://`, then one or
more characters that are not `/`, `?`, `#`, `\` or white space, then `/`.
The closing `/` is required: what is joined after it is path, query or
fragment and cannot move the request, whereas `"https://api.example.com" +
x` can be `https://api.example.com@evil.example/`. A URL that matches
neither way sets `any`, as before. Until 0.13.0 every URL that was not one
literal set `any`; an audit of the same program is therefore narrower under
0.13.0, never wider.

### 8.3 How safe_command is derived

For each name in `effects`, in order:

- `ffi`: `ffi:` followed by `ffi_modules` joined with commas when
  `ffi_modules` is not empty (the continuation form of section 4.2);
  otherwise `ffi`.
- `fs`: for `read` and then `write`: `fs:read` when `read_any` is true,
  otherwise one `fs:read:P` for each path P in `read`, with `, @ [ ] %`
  in P percent-encoded (section 5.1); and the same for `write`. If this
  produced nothing, `fs`.
- `net`: `net` when `any` is true or `hosts` is empty; otherwise one
  `net:E` for each entry E of `hosts`, an IPv6 host bracketed and any
  `, @ [ ] %` in a host percent-encoded (section 5.2). Each `net_hosts`
  entry is already in this form.
- any other name: the name itself (always an effect of section 3.1,
  since `effects` holds no other name, section 3.2).

The results are joined with commas. Because the paths and hosts are
escaped and every name is an effect, `safe_command` always parses,
whether or not `ok` is true, and `parse_budget` of it reproduces the
grants it was built from.

**What this section defines is the grant list.** A producer may put its
own command in front of it - the reference writes `sabline <file>
--allow ` and wrote `velaris <file> --allow ` before 0.14.0 - and that
prefix is the producer's, not this document's. A conformance case
therefore compares the grants and not the whole string *(0.14.0; until
then the corpus compared the string, which required every implementation
to be called what the reference was called)*.

### 8.4 What an audit does not tell you

- **It reads literals only.** A path, URL or module named by a value
  built at runtime is reported through `read_any`, `write_any`, `any`
  and - from sabline-lang 4.0 - `ffi_any`, not listed. A program whose
  `ffi_modules` is `["math"]` and whose `ffi_any` is true also calls a
  module whose name it builds while running; under the `safe_command`'s
  `ffi:math` that call is refused (E311), so `safe_command` still errs
  toward refusal, and section 9 takes such a program to need unscoped
  `ffi`.
- *Resolved in 0.3 (sabline-lang 4.0.0).* Version 0.2 recorded that
  nothing in `sabline.audit/1` said a module was named by a computed
  value, so a reader of the audit was not told such a call existed.
  `ffi_any` is added within version 1, as an optional field, closing
  open question Q4. A document from a producer before 4.0 lacks it, and
  says nothing either way.
- **`safe_command` is the narrowest budget the audit can write, not a
  budget known to be enough, and not one known to be safe.** It grants
  every declared effect, `ffi` included, and a relative path in it
  resolves against the working directory of whoever runs the command.
- *Resolved in 0.2 (sabline-lang 3.3.0).* Version 0.1 recorded that in
  sabline-lang 3.1.1 `safe_command` was wrong in three cases: an IPv6
  literal host written without brackets (`net:::1`) parsed as a
  different host; a path literal containing `,` or `@` produced text
  that did not parse, or parsed as something else; and an unknown name
  in a declaration was copied into it. From 3.3.0 IPv6 hosts are
  bracketed and `, @ [ ] %` are percent-encoded in paths and hosts
  (sections 5.1, 5.2), so `safe_command` round-trips; and an unknown
  name in a `uses` clause no longer compiles (section 3.2). This closes
  open question Q5. It left one case, found in 0.4: the audit that
  reports that E300 still copied the name into `safe_command` until
  sabline-lang 4.1.0 (section 3.2).
- **A count is a bound the text fixes, not a measurement.** When `ok`
  is true, `counts` is at least the operations any one call to a
  function defined in the file can perform (section 9.4), and may be far
  more; `null` says the text fixes no bound, not that the program
  performs many. Like `effects`, it does not cover a `main` the file
  imports from another file.
- **When `ok` is false, no field bounds anything.**

### 8.5 The audit as an in-toto predicate

*New in 0.4.* A `sabline.audit/1` document names no artifact and
carries no signature, so on its own it cannot say which source file it
describes or who says so. This section defines an in-toto attestation
predicate type that binds an audit to the digests of the files audited,
so that a signed in-toto Statement can say it. It closes open question
Q11.

**Predicate type:**
<https://sabline.dev/capability/v1>. That URL is where the type's
description and schema are published, on the reference's documentation
site, and it resolves to them.

**Also accepted for verification:** two earlier names of this same type,
in the order they were used:

- `https://velaris-lang.dev/capability/v1`, its name from 0.11.0 until
  0.14.0, which sabline-lang 8.3.0 to 8.5.0 wrote;
- `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`, its
  name until 0.11.0, which sabline-lang 4.2.0 to 8.2.1 wrote.

Both addresses now redirect to the one above. A consumer SHOULD read a
Statement naming either as a Statement of this type, and MUST NOT read a
Statement of any other type as one of this type. A producer MUST write the
name above. Nothing is ever removed from this list: a name that was
published and signed goes on being accepted, and a new name joins it.
*Changed in 0.14.0*: the reference implementation was renamed from Velaris
to Sabline, because the name Velaris belongs to an unrelated company
(velaris.io), and its project holds sabline.dev. *Changed in 0.11.0*: the
project took a domain of its own, where the name before that was an
address under its maintainer's account name. Neither `velaris.dev` nor
`velaris.io` has ever been this type's domain, and neither names any type
this document defines.

A Statement of this type is an in-toto Statement v1
(<https://github.com/in-toto/attestation>):

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    {"name": "examples/effects.vel", "digest": {"sha256": "..."}}
  ],
  "predicateType": "https://sabline.dev/capability/v1",
  "predicate": {
    "producer": {"name": "sabline-lang",
                 "uri": "https://github.com/gowrishankar-infra/sabline-lang"},
    "specification": "sabline-spec 0.5",
    "auditedAt": "2026-09-11T00:00:00Z",
    "audit": {"schema": "sabline.audit/1", "...": "..."}
  }
}
```

- **`subject`.** The first subject MUST be the file audited: its `name`
  is its path as the producer was given it, `/`-separated, and its
  `digest` MUST include `sha256` of its bytes. The files it imports
  SHOULD follow, one subject each, since `ffi_modules`, `ffi_any`,
  `fs_paths` and `net_hosts` read them too (section 8.2). A producer
  MUST produce the audit from exactly the bytes the digests name.
- **`predicate.audit`** (required): a `sabline.audit/1` document, as
  section 8 defines it and
  [schemas/velaris.audit.1.schema.json](schemas/velaris.audit.1.schema.json)
  checks.
- **`predicate.producer`** (required): `name`, the implementation that
  wrote the audit, and optionally `uri`. Its version is the audit's
  `sabline_version`.
- **`predicate.specification`** (optional): the version of this
  document the producer followed, as `sabline-spec 0.5`.
- **`predicate.auditedAt`** (optional): when the audit was made, RFC
  3339 in UTC, as the producer's clock says.
- **`predicate.conformance`** (optional): `levels`, the levels of
  [CONFORMANCE.md](CONFORMANCE.md) the producer claims, and `corpus`,
  the corpus it ran. A claim, not evidence.

The predicate's schema is
[schemas/capability-predicate.v1.schema.json](schemas/capability-predicate.v1.schema.json);
the reference publishes the same file at the predicate type's URL, and
`tools/check_sync.py` fails if the two differ.

**Parsing rules.** In-toto's standard parsing rules apply, the
monotonic principle included. A consumer MUST ignore a field it does
not know, in the predicate and in the audit (section 8.1). Fields may
be added within v1; a change of meaning is a new predicate type,
`.../capability/v2`. A consumer MUST check that the first subject's
digest is the digest of the file it means to trust.

**What a Statement of this type says**, when its signature verifies:
that the signer ran the named producer on the bytes the subjects name
and got this audit. It does not say that the audit is right, that the
program is safe to run, or that any runtime will enforce the budget in
`safe_command`; and when `audit.ok` is false it says nothing about what
the program may do (section 8.4).

*Resolved in 0.5 (sabline-lang 4.2.0).* Version 0.4 recorded that the
reference published the predicate type and its schema and wrote no
Statements of it, and its example Statement was assembled by hand from
`sabline audit FILE --json` and the file's digest. From 4.2.0 the
reference writes them:

- `sabline attest FILE` writes one Statement. Its subjects are FILE,
  then each file it imports, by the sha256 of the bytes the audit read;
  a file that changes while it is being attested is refused. Its
  `predicate.audit` is `sabline.audit(source).as_dict()` itself, not a
  copy, so it holds what the audit holds and nothing more. It sets
  `producer`, `specification` and `auditedAt` - from
  `SOURCE_DATE_EPOCH` when that is set - and not `conformance`.
- `sabline attest DIR` writes one Statement for each `.vel` file under
  DIR that section 9.3 takes as a program, one to a line (JSON Lines,
  the layout of an in-toto Bundle, whose lines are envelopes once
  signed): a Statement of this type carries one audit, so a directory
  is several.
- Where the audit could not determine something, the Statement says so
  in the audit's own fields, unchanged: `ok` false with its `problems`,
  `ffi_any`, `read_any`, `write_any` or `any` true, `counts` or one of
  its entries `null`, `prover` false.
- It signs nothing. The reference's release workflow signs one
  Statement, for its `examples/effects.vel`, with cosign and with
  sigstore-python, and verifies both before publishing them.

[examples/capability-statement.json](examples/capability-statement.json)
is the Statement `sabline attest examples/effects.vel` writes in
sabline-lang at tag `v4.2.0`, with `SOURCE_DATE_EPOCH` set to that
commit's time, as the release workflow runs it. It names the type by its
earlier name, as every Statement of that release does.

### 8.6 secrets

*New in 0.7 (sabline-lang 6.0.0).* `secrets` is an object added to
`sabline.audit/1` within version 1, so a consumer that does not know
it ignores it (section 8.1) and a producer that does not implement the
reference's `Secret of T` writes it with empty values.

| Field | Type | Meaning |
|---|---|---|
| `sources` | array of strings | sorted, without repeats: the name of every builtin the program as loaded reaches that returns a value the type system will not let the program emit. In the reference: `env`, `read_file_secret` and, from 0.13.0, `tool_secret` (sabline-lang SPEC.md section 3.1). |
| `declassifies` | boolean | true when the program as loaded contains at least one call to `declassify` |
| `declassifications` | array | one object per such call, each with `reason` (the text written in the call), `function` (the name of the function the call is in) and `line` (integer). Sorted by `function`, then `line`, then `reason`. Empty when `declassifies` is false. |

**A MAC under a secret key** *(0.13.0, sabline-lang 8.5.0)*. The reference
has two operations that take such a value as a key and give back an
ordinary one: `hmac_sha256(key, message)`, the HMAC-SHA256 of the message
under the key as lowercase hexadecimal, and `hmac_sha256_chain(key,
messages)`, which applies it once for each message, each result's 32 bytes
the next key. A signature is sent in the clear, so its result carries no
mark; that makes each a way out, and each is held as `declassify` is. It is
an operation of the `declassify` effect (section 3.1). `declassifies` is
true when the program as loaded contains a call to either. Each call has an
entry in `declassifications` with `reason` the fixed text `hmac signature`,
`function`, `line`, and `builtin`, the operation's name; an entry for
`declassify` has no `builtin`. The key MUST be such a value and the message
MUST NOT carry one, or the program does not compile. A consumer that reads
only `hmac signature` reasons is reading a program that signs; a consumer
SHOULD still read where the key comes from, because an operation over such
a value gives such a value, and a MAC under a key a program derived from a
credential - one character of it - can be matched against guesses.

The whole field is `null` when the program could not be loaded, as when
it does not parse; then nothing was determined. It is **not** null
merely because `ok` is false: a program refused for handing a secret to
something that emits it still reports the sources that made the secret,
which is what a reader wants at that moment.

**What it is for.** A consumer asks one question - *does this program
ever let a secret out* - and `declassifies` answers it without running
the program. `false` means the values those builtins returned reach
nothing that emits them, by the static rule sabline-lang SPEC.md
section 3.1 states: no operation that emits and no operation that can
fail takes one, every operation over one gives one, and no branch is
taken on one. `true` means a secret may leave, and
`declassifications` says where and with what stated reason.

**What it does not say.**

- It does not say the reasons are true. A reason is text a program's
  author wrote; nothing checks it.
- It is not a non-interference result. It says nothing about what a
  program controls that is not a value - how long it runs, how much it
  allocates, whether it stops at all - nor about what an operator can
  learn by running the same program many times. In sabline-lang 6.0.0
  this bullet said more: a comparison over such a value gave an
  ordinary boolean, so a program with `declassifies: false` could read
  a secret out a character at a time and print it. 7.0.0 closed that,
  and the bullet is narrowed to what is still true.
- It covers only values those builtins produced. A secret a program
  receives some other way - standard input, its arguments, the network,
  the host language - is an ordinary value, and `sources` says nothing
  about it.
- `declassify` is an effect, so it is in `effects` and in
  `safe_command` like any other (sections 3.1, 8.3), and an operator
  can run the program without granting it. Withholding the grant makes
  each `declassify` a refusal at the moment it is reached, not a
  compile error: the program stops there.

### 8.7 sabline.receipt/1, a record of one run

*New in 0.10.0 (sabline-lang 8.1.0).* An audit (section 8) and the
Statement of section 8.5 say what a program may do, before it runs.
A receipt says what one run of it did: the budget it was given, each
refusal, each declassification with the reason written for it, the
parameters it ran under, how it ended and how long it took. It is bound to
the files that ran by the same digests section 8.5 uses, so an audit of a
program and a receipt of one of its runs can be matched by those digests.

**Predicate type:**
<https://sabline.dev/receipt/v1>. That URL is where the type's
description and schema are published, on the reference's documentation
site. **Also accepted for verification:**
`https://velaris-lang.dev/receipt/v1`, its name from 0.11.0 until 0.14.0,
which sabline-lang 8.3.0 to 8.5.0 wrote, and
`https://gowrishankar-infra.github.io/velaris-lang/receipt/v1`, its name
until 0.11.0, which sabline-lang 8.1.0 to 8.2.1 wrote - each read as
section 8.5 reads the earlier names of its type;
[schemas/receipt-predicate.v1.schema.json](schemas/receipt-predicate.v1.schema.json)
is the schema, and `tools/check_sync.py` fails if the published copy
differs.

A receipt is an in-toto Statement v1 of that type:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    {"name": "examples/effects.vel", "digest": {"sha256": "..."}}
  ],
  "predicateType": "https://velaris-lang.dev/receipt/v1",
  "predicate": {
    "schema": "sabline.receipt/1",
    "producer": {"name": "sabline-lang", "version": "8.1.0"},
    "wall_time_ms": 41.7,
    "budget": "clock,fs:read:/work/report.txt,fs:write:/work/report.txt,io,rand",
    "run_parameters": {"seed": null, "freeze_time": null, "timeout": null,
                       "max_memory_mb": null, "confinement": "full",
                       "confinement_reason": "the operating system holds every file, network and process limit of this budget",
                       "confinement_layers": ["landlock-abi4", "seccomp"],
                       "os_policy_sha256": "2702413c15253be6589ce6f39dbfbb129c9578d6ce62576d996f895b6faa9994"},
    "effects_used": {"clock": 1, "fs": 2, "io": 4, "rand": 1},
    "refusals": [],
    "declassifications": [],
    "exit": {"status": 0, "outcome": "ok", "code": null},
    "complete": true
  }
}
```

- **`subject`.** The first subject MUST be the program that ran: its
  `name` is its path as the producer was given it, `/`-separated, or
  `<source>` for a program given as text with no file, and its `digest`
  MUST include `sha256` of the exact text that ran, as UTF-8. The files it
  imported SHOULD follow, one subject each, by the sha256 of their bytes
  and named as section 8.5 names them. For the same bytes a producer
  SHOULD write the subjects a Statement of section 8.5 writes.
- **`predicate`** is a `sabline.receipt/1` document:

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | `"sabline.receipt/1"` |
| `producer` | object | `name` of the implementation that ran the program, and optionally `uri` and `version` |
| `specification` | string | optional: the version of this document the producer followed, as `sabline-spec 0.10.0` |
| `startedAt` | string | optional: when the run started, RFC 3339 in UTC, by the producer's clock |
| `wall_time_ms` | number | how long the run took, in milliseconds, by the producer's clock |
| `budget` | string | the budget the run was given, in the grammar of section 4 |
| `run_parameters` | object | `seed` (integer or null) and `freeze_time` (RFC 3339 or null), which fix the run's randomness and clock; `timeout` (seconds or null) and `max_memory_mb` (integer or null), the limits it ran under; optionally `max_read_bytes`; and `confinement`, a word for the operating-system confinement the run had - `"none"` when the budget was the only boundary. From 0.12.0 the word is a level: `"full"` when the operating system held every file, network and process limit of the budget, `"partial"` when it held some, `"none"` when it held nothing; and three optional fields say more - `confinement_reason`, text naming each limit that was not held and why (or why nothing was asked); `confinement_layers`, an array of the producer's names for the mechanisms it applied; and `os_policy_sha256`, the lowercase hex sha256 of the policy the producer derived from the budget and asked the operating system to hold, or null. A receipt written before 0.12.0 has none of the three, and its `confinement` is `"none"` or names a mechanism (section 8.9). Optionally, from 0.11.0, `profile`, the name of a profile the run was held to beyond its budget, as `"eval"` (section 8.9) |
| `effects_used` | object or null | each effect and how many operations of it the budget let through; `null` when the producer could not tell, as when the run was stopped from outside |
| `grants_used` | array | optional, from 0.13.0: one object per grant of the budget that let at least one operation through - `grant`, the grant as canonical text (section 4.7), without a count; `times`, how many operations it let through. Sorted by `grant`. It is the operator's text and MUST NOT hold the path, host, module or argument the program gave: `net:api.example.com:443`, never the URL. An operation is counted under the first grant, in the budget's order, that permits it |
| `refusals` | array | one object per distinct refusal: `code`; `effect`, one of the nine names of section 3.1, or null; `line`; `stopped`, whether the refusal ended the run (a redirect refused under section 6 G4 does not); `times` |
| `declassifications` | array | one object per distinct declassification: `reason`, the text written in the program; `line`; `times`. From 0.13.0 a MAC under a secret key (section 8.6) is one, with `reason` the text `hmac signature` and `key_fingerprint`: twelve lowercase hexadecimal digits by which a reader tells one key from another and the same key from run to run - in the reference, the first twelve of the sha256 of the bytes `sabline key fingerprint`, a zero byte, and the key - or the text `many`, which a producer writes for a call site once it has named sixteen keys there. It is a function of the key and MUST NOT be reversible to it for a key of a credential's entropy; a producer MUST NOT write the key or the MAC |
| `tool_calls` | array | from 0.13.0, present only for a run that was given a manifest of tools (section 8.10): one object per place a tool was called - `tool`, its name; `line`; `times`; `secret`, whether the manifest marks its result secret; `held_to`, the budget's and the manifest's items, as canonical text, whose patterns held its arguments. It MUST NOT hold the arguments or the result |
| `tool_ceiling` | object | from 0.13.0, present with `tool_calls`: `calls` and `cost`, the manifest's ceiling on each (a number or null); `unit`, the manifest's name for its cost unit; `calls_used` and `cost_used`, what the run spent; `manifest_sha256`, the lowercase hex sha256 of the manifest's bytes |
| `exit` | object | `status`, the exit status the producer reported (integer or null); `outcome`, one of `ok`, `refused`, `failed`, `did_not_compile`, `timeout`, `out_of_memory`; `code`, the code of the error that ended the run, or null |
| `stop` | object | optional, from 0.11.0: present when a stop was asked for from outside the run - `asked`, what asked; `honoured`, how it was honoured; `after_ms`, when it was asked, from the run's start; `grace_seconds` (section 8.9) |
| `complete` | boolean | false when the run was stopped from outside before it could report. What is listed happened, and each `times` is at least the number given |

**What a receipt MUST NOT hold.** A producer MUST NOT put in a receipt a
value the program handled: not its output, its input, its arguments or its
environment; not a message that quotes one; not the path, host or module a
refused operation named, which the program may have built from a value it
declassified; not a declassified value. A refusal is its code, its effect
and its line; a declassification is the reason written in the program (in
the reference a literal, E561).

**What it does not hide.** A receipt records what a program did, and a
program controls some of that without handing the receipt a value: its
exit status, the line at which it was refused or stopped, how many times
it did something, and how long it ran. A program that has declassified a
value may choose any of these from it. A consumer that must not learn a
declassified value from a receipt must not grant `declassify` - the same
advice section 8.6 gives about output.

**What a receipt says**, when its signature verifies: that the signer ran
the named producer on the bytes the subjects name, under this budget and
these parameters, and saw this run. It does not say the run was confined
by more than the budget unless `confinement` says so; it is no stronger
than the machine the producer ran on; and it says nothing about any other
run of the same program.

**Parsing rules** are those of section 8.5: in-toto's, the monotonic
principle included; fields may be added within v1, and a consumer MUST
ignore a field it does not know; a change of meaning is `.../receipt/v2`.

*Reference behaviour (sabline-lang 8.1.0).* The reference writes a
receipt for every run through `sabline.run` and `sabline.Pool.run`, as
the result's `receipt`; for `sabline program.vel --receipt FILE`; and for
a run through its HTTP door or MCP server when the request asks
(`"receipt": true`). A run killed by its time or memory limit still has a
receipt, marked incomplete, holding what its worker reported before it was
killed. The reference signs none; its release workflow signs one, for the
run of `examples/effects.vel` whose Statement of section 8.5 it also signs,
with cosign and with sigstore-python, and verifies both.
[examples/run-receipt.json](examples/run-receipt.json) is a receipt the
reference wrote for that run, and
[examples/refused-receipt.json](examples/refused-receipt.json) one it
wrote for the same program given no `fs`, which stopped at its first
refusal. Both name the type by its earlier name, as every receipt
sabline-lang 8.1.0 to 8.2.1 wrote does.

### 8.8 Comparing receipts

*New in 0.11.0 (sabline-lang 8.3.0). The document this section describes
is provisional.* A receipt names no path a run read and no host it reached:
what it names is what the run was granted (`budget`), what it used
(`effects_used`), what was refused and what was declassified. Two
comparisons follow from that, and neither runs anything.

**Against an audit** of the program (section 8), or a Statement of section
8.5, a difference is:

- an effect in `effects_used` with a count above zero, or the effect of a
  refusal, that the audit's `effects` does not hold;
- a host of the budget's `net:` grants that `net_hosts.hosts` does not name
  (a host granted with a port is named by the same host with that port, or
  with none); not compared when `net_hosts.any` is true;
- a path of the budget's `fs:` grants in which `fs_paths` names no path of
  that direction; not compared when `read_any` or `write_any` is true. A
  path in a budget is absolute on the machine that ran it and a path in an
  audit is as the program wrote it, so a granted path is named when it ends
  with a path the audit names, or with a directory holding one;
- a module of the budget's `ffi:` grants that `ffi_modules` does not name;
  not compared when `ffi_any` is true;
- a declassification whose reason and line `secrets.declassifications` does
  not hold;
- an `fs` or `net` count above the audit's `counts` bound, where that bound
  is a number;
- where the audit comes with subjects (a Statement of 8.5), a receipt whose
  first subject's digest is not the audit's first subject's, or which names
  a digest the audit's subjects do not.

**Against earlier receipts** of the same subjects - the same set of
digests; a receipt of other subjects is not compared - a difference is a
host, a path or a module granted, or an effect used, that no earlier receipt
has; a count in `effects_used` above the largest any earlier receipt holds
for that effect; a declassification when no earlier receipt has one; and a
declassification reason no earlier receipt holds.

The reference writes the result as `sabline.receipts-diff/1`:

```json
{
  "schema": "sabline.receipts-diff/1",
  "receipt": "run.json",
  "subjects": [{"name": "task.vel", "digest": {"sha256": "..."}}],
  "against_audit": {
    "source": "the audit of task.vel",
    "differences": [{"kind": "host", "what": "collector.example.org:443",
                     "detail": "the budget granted it; the audit names no such host"}],
    "not_compared": []
  },
  "against_receipts": {
    "compared": ["earlier.json"],
    "left_out": [{"file": "other.json", "why": "a receipt of other subjects"}],
    "differences": [{"kind": "count_above_maximum", "what": "fs",
                     "detail": "9 fs operation(s); the most in an earlier run was 1"}]
  },
  "problems": [],
  "differences": 2,
  "exit": 1
}
```

`kind` is `effect`, `host`, `path`, `module`, `declassification`, `count` or
`subject` against an audit, and `new_host`, `new_path`, `new_module`,
`count_above_maximum`, `first_declassification` or `new_declassification`
against earlier receipts. The exit status is 0 with no difference, 1 with
any, and 2 when a comparison could not be made: a file that is not a receipt
of a type this document defines, an audit that cannot be read, or no earlier
receipt of the same subjects.

**What a comparison does not say.** A receipt is a claim, and comparing
claims does not make them true: a receipt edited to omit an effect compares
clean against an audit that has it. Receipts compared as signed Statements,
matched by their subjects, say what their signers saw.

### 8.9 A run under an evaluation profile

*New in 0.11.0 (sabline-lang 8.3.0).* A receipt whose
`run_parameters.profile` is `"eval"` records a run held to a profile beyond
its budget. A producer that writes that name MUST have held the run to all
of:

- no `net`, `ffi` or `env` in the budget, and no `fs` grant without a path;
- a time limit and a memory limit (`timeout` and `max_memory_mb` not null);
- the receipt written where no `fs` grant of the budget reaches, or sent to a
  URL;
- a stop asked for from outside the run honoured - at the next point the
  program can see it, or by ending the run after a grace period - and
  recorded in `stop`.

`run_parameters.confinement` says what operating-system confinement was
applied, not what was asked for. *Changed in 0.12.0 (sabline-lang 8.4.0).*
It is a level - `full`, `partial` or `none` (section 8.7) - and a producer
that writes the profile's name from 0.12.0 on MUST NOT have run the program
at `none`: the reference refuses to start such a run. The mechanisms are
named in `confinement_layers`; the reference writes `landlock-abiN` and
`seccomp` on Linux, `sandbox-profile` on macOS, and `job-object`,
`token-privileges-removed` and `low-integrity` on Windows, and its
THREAT_MODEL.md has the table of what each holds for each grant. Until
0.12.0 the reference wrote a mechanism in `confinement` itself -
`landlock-net`, `landlock`, `job-one-process`, `sandbox-exec` - or `none`,
ran the program under the budget alone where it got `none`, and confined no
reads; a consumer reading an earlier receipt takes those words as they
were.

`stop`, when present, has `asked`, what asked for the stop (a signal, or a
stop file appearing); `honoured`, one of `at a call or loop turn`, `worker
killed after the grace period` or `the run had already ended`; `after_ms`,
when it was asked, from the run's start; and `grace_seconds`. A run stopped
at a call or loop turn has `exit.code` `E615` and `complete` true; a run
whose worker was killed has `exit.code` `E615` and `complete` false.

### 8.10 sabline.tools/1, a manifest of tools (provisional)

*New in 0.13.0 (sabline-lang 8.5.0). Provisional: its fields, and what
travels between a run and its host, may change in a minor version of this
document until one says otherwise. The `tool` effect, its grants (sections
3.1, 4.1 and 5.6) and what a receipt records (section 8.7) are not
provisional.*

A process that hosts a run gives it a manifest: which tools there are, and
what the host will accept and spend.

```json
{"schema": "sabline.tools/1",
 "tools": {
   "search": {"description": "Look a phrase up.",
              "arguments": {"type": "object",
                            "properties": {"query": {"type": "string"}},
                            "required": ["query"]},
              "result": "text", "cost": 1}},
 "allow": ["tool:search@20"],
 "ceiling": {"calls": 25, "cost": 40, "unit": "credits"}}
```

| Field | Meaning |
|---|---|
| `tools` | an object, one entry per tool, keyed by its name (section 5.6) |
| `tools.T.arguments` | a JSON Schema for the call's arguments, which are one object. A producer MUST refuse a manifest that uses a keyword it does not check; the reference checks `type`, `properties`, `required`, `additionalProperties`, `items`, `enum`, `const`, `minLength`, `maxLength`, `minimum`, `maximum`, `minItems` and `maxItems`, and reads `additionalProperties` as false when it is not given |
| `tools.T.result` | `"text"` (the default) or `"secret"`: a secret result is a value the type system will not let the program emit (section 8.6), and the program MUST ask for it as one |
| `tools.T.cost` | what one call spends, a number, 0 or more; 0 when absent. The unit is the host's |
| `allow` | optional: `tool` items in the grammar of section 4, the host's own. A call MUST pass them and the run's budget |
| `ceiling` | optional: `calls` and `cost`, the most one run may spend of each, and `unit`, a name for the cost unit |

A call is made only when, in this order: the manifest offers the tool; the
arguments are one JSON object the tool's schema accepts, and a tool whose
result is secret is asked for as one; the budget's tool items and then the
manifest's `allow` permit it (section 5.6); no count of section 5.6 is
passed; and the ceiling's calls and cost, counting this call's `cost`,
would not be passed. Otherwise it is refused - in the reference E320, E323,
E321, E322 and E322 - the run ends, and the host is not asked. When the
host's answer gives a cost, that cost is what is counted, so a run may end
past its cost ceiling by one call's difference; the next call is refused.

What a tool returns is a value like any other. Nothing in this version
marks it as the host's words rather than the program's, so a result can
direct what a program does inside its budget, and cannot take it outside.
A later version will define that mark.

The reference exchanges calls and answers as JSON objects, one to a line,
on the run's standard input and output (sabline-lang EMBEDDING.md,
`sabline.tools-door/1`). That exchange is the reference's and is not part
of this format.

## 9. sabline.capabilities/1

*Resolved in 0.3 (sabline-lang 4.0.0).* Versions 0.1 and 0.2 defined a
provisional `sabline.capabilities/0` that no implementation read or
wrote. From 4.0.0 the reference writes and reads the document this
section defines, `sabline.capabilities/1`, and the section is no longer
provisional. `/1` keeps `/0`'s grant grammar, covering rule and
per-program entries, and adds what `/0` could not express: the
repository's whole surface, a bound on operations, the effects of each
function, and the version and date of the producer. The `/0` schema is
kept in `schemas/` for the record; no reference version wrote a `/0`
document, and the reference refuses to compare against one.

### 9.1 What it is for

A repository commits a baseline declaring the capability surface its
programs may have. A check in CI derives the surface the working tree
needs and fails when it is wider. Its purpose is change made a little
at a time: capability assembled across many commits, each of which
looks harmless to a reviewer reading its diff - a helper that builds a
URL, a function that reads a file, then a call three levels down that
sends one to the other. Capability is binary and cumulative, so the
sum of those steps reaches exactly as far as one step that did it all
at once; but only a comparison with a declared baseline sees the sum.
A comparison of each commit with the one before it sees each step
alone, and once a widening has been merged, sees nothing at all.

So the rule of this section: **a check compares the tree with the
baseline, and with nothing else.** A widening, once introduced, fails
every later check until the baseline itself is edited - which is a
change to a file, made by a person, visible in review.

A baseline records what programs' text needs, not what a run may do.
It is not a budget, though its grants are written in the budget
grammar, and a program's grants joined with commas, with its counts
appended, make a budget an operator may choose to run under.

### 9.2 The document

A JSON object:

| Field | Meaning |
|---|---|
| `schema` | `"sabline.capabilities/1"` |
| `sabline_version` | the version of the producer that wrote it. Informative: a checker of another version SHOULD warn, and MUST NOT fail for that reason alone |
| `date` | the day it was written, `YYYY-MM-DD`, UTC. Informative |
| `surface` | the repository's surface: `grants`, an array of grants, and `counts`, an object (below) |
| `programs` | an array of program entries, sorted by `file`, no two with the same `file` |

A program entry is one of two shapes:

| Shape | Fields |
|---|---|
| a program that compiled | `file`; `grants`, an array; `counts`, an object; `functions`, an object mapping the name of each function the file defines (inline function values are not listed) to the sorted array of effects it declares |
| a program that did not | `file`, and `compiles`: `false` |

`file` is the program's path relative to the directory holding the
baseline: `/`-separated, not beginning with `/`, with no empty, `.` or
`..` component, and no `\`.

`counts` has at most two keys, `fs` and `net`. A key's value is a whole
number N - at most N operations of that effect in one run, derived as
section 9.4 says - or `null`, meaning the text sets no bound. An effect
with grants in the same list and no key in `counts` has no bound, as a
budget with no count has none (section 5.4).

Grants use the grammar of section 4, with these restrictions so that a
grant means the same on every machine:

1. **No counts** in a grant; counts are in `counts`.
2. **One module per grant**: `ffi:math` and `ffi:json`, never the
   continuation form.
3. **Paths as the program writes them**, compared as text (section 9.5)
   and never resolved against a file system. No `,` or `@` in a path.
4. **Hosts lower case**, IPv6 addresses in brackets.
5. **Reduced**: sorted by code point, no repeats, and no grant that
   another grant in the same list covers (section 9.5). Of two grants
   that cover each other - two spellings of one path - the first in
   code-point order is kept.

Within version 1, fields may be added. A consumer MUST ignore a field
it does not know. The schema,
[schemas/velaris.capabilities.1.schema.json](schemas/velaris.capabilities.1.schema.json),
checks the shape; it cannot check sorting, reduction or the port
range, which `tools/validate.py` checks for the first two.

### 9.3 From a program's text to what it needs

Each `.vel` file under the directory holding the baseline is a program,
except files inside a `.git` directory and, where that directory is in
a git work tree, files git ignores. For each:

1. **Load and check it.** Read the file and everything it imports, and
   run the checks that need no prover: the rules of section 3.2, the
   shape of `main`, and the language's type rules. If loading or a
   check fails, the program *does not compile*: its entry is
   `{"file": ..., "compiles": false}` and it needs nothing, since it
   cannot run. The prover does not take part, so the result is the
   same with and without one.
2. **Its functions** are those the file defines, not counting inline
   function values - plus `main`, when the file imports its `main`
   from another file instead of defining one, because running the file
   runs that `main`.
3. **Its effects** are the union of its functions' declarations.
4. **Fixed text.** An argument is *fixed* when it is a text literal; or
   a variable of the calling function that is bound exactly once, by a
   `let` whose value is fixed text, and is never assigned, bound by a
   `check`, or a parameter; or `+` of two fixed texts. Any other
   argument is *built while running*.
5. **What its calls name**, read over every function loaded - its own
   and every imported file's, as `sabline.audit/1` reads them (section
   8.2): the paths given to `read_file` and `file_exists` (read) and to
   `write_file` (write); the `net_hosts` entry (section 8.2) of the URL
   given to `fetch`, `post` or `fetch_status`, or as the second argument
   of `request`; the module given to `py`, `py_int`, `py_float`,
   `py_json` or `py_new`, up to its first `.`; and, from 0.13.0, the tool
   given to `tool` or `tool_secret`. For each of the four, a flag says some
   such argument was built while running. From 0.13.0 a URL whose
   beginning is fixed text that holds the `/` ending its host names that
   host (section 8.2), where fixed text is as step 4 has it.
6. **Its grants.** For each effect e in step 3, in order:
   - `io`, `env`, `clock`, `rand`, `declassify`: e.
   - `tool`: one `tool:T` for each tool named, or `tool` alone when a tool
     argument was built while running, when none was named, or when a name
     is not one section 5.6 allows. A baseline records which tools, never
     their arguments: a grant that holds an argument is not a baseline grant.
   - `ffi`: one `ffi:M` for each module named, or `ffi` alone when a
     module argument was built while running, when none was named, or
     when a module named is empty or holds `,`, `@`, `:` or whitespace.
   - `fs`: for each direction d, `read` then `write`: `fs:d` alone when
     a path argument for d was built while running, or a path for d is
     empty, holds `,`, `@`, a tab, a line break, or leading or trailing
     whitespace; otherwise one `fs:d:P` for each path P named for d.
     If this produced nothing, `fs`.
   - `net`: `net` alone when a URL argument was built while running,
     when no host was named, or when an entry holds `*` or `/`, or more
     than one `:` outside brackets; otherwise one `net:E` for each
     entry E.

   Then reduce (section 9.2, rule 5). Wherever the text cannot fix a
   scope, the grant is unscoped - wider - so a scoped baseline does not
   cover it and someone has to look.
7. **Its counts**: for `fs` and for `net`, when step 3 includes it, the
   largest bound (section 9.4) of any of its functions (step 2). For a
   file with a `main` that calls every other function, this is the
   bound on one run.
8. **Its `functions`**: each function the file defines, with its own
   declaration, sorted.

The **surface** of a tree is the union of the grants of its programs
that compile, reduced, and for `fs` and `net` the largest count any of
them has, `null` exceeding every number.

The reference's `sabline.audit/1` reads literals only (section 8.4);
step 4 reads fixed text, so moving a literal into a variable bound once
does not change what a program needs.

### 9.4 A bound on operations

An *operation* is a call to `read_file`, `write_file` or `file_exists`
(an `fs` operation) or to `fetch`, `post`, `fetch_status` or `request`
(a `net` operation) - exactly the calls a runtime counts against a
budget's count (section 5.4). For a function f and each of the two
effects, B(f) is the most operations of that effect one call to f can
perform, a whole number or infinity:

- **An expression** is the sum over the calls inside it: a call adds 1
  when it is an operation of that effect, plus B of the callee when it
  calls a function of the program. An inline function value adds
  nothing: it is pure (section 3.2, T4).
- **Statements in sequence** add. `let`, assignment, `return`, `fail`
  and an expression statement count their expression. `if` counts its
  condition and the larger of its two branches; `check` counts its
  subject and the larger of its two arms. Both `and` and `or` count
  both sides.
- **A loop** `while C { S }` that turns at most T times counts C T+1
  times and S T times, where zero times infinity is zero. T is the
  smallest of the bounds its condition gives, and infinity when it
  gives none. A conjunct `v < E`, `v <= E`, `v > E` or `v >= E` of C (v
  on either side) gives a bound when: v is assigned in S; every path
  through S that reaches its end moves v by exactly one step toward E
  and assigns it nowhere else (the termination rule of sabline-lang
  SPEC.md section 9.5); and v's value s on entry to the loop, and E's
  value l, are known (below). The bound is then l − s for `<`,
  l − s + 1 for `<=`, s − l for `>` and s − l + 1 for `>=`, or 0 when
  that is negative. When every path through S leaves the loop by
  `return` or `fail`, the bound is 1. A `for` loop is the `while` loop
  it stands for (sabline-lang SPEC.md section 9.5).
- **Known values.** Walking a function's statements in order, a `let`
  or assignment whose value is built from whole-number literals, known
  variables, negation, `+`, `-` and `*`, or is `length` of a list
  literal, or of a variable known to hold a list literal of n items,
  makes the variable known; a `let` or assignment of a list literal
  makes it known to hold that many items; any other `let` or
  assignment forgets the variable. After an `if`, a `check` or a loop,
  every variable bound inside it is forgotten. A loop's body starts
  from the values known on entry, less the variables the body binds,
  and E's value is taken only from those.
- **Recursion.** A call to a function whose bound is still being
  computed contributes infinity for each counted effect that function
  declares.

A bound greater than 2^53 is written as `null`. The rules give a bound
at least as large as the operations any run can perform, for a
program that compiles; they do not try to be tight, and a loop whose
turns the text does not fix has none.

### 9.5 When one grant covers another

A grant b covers a grant c when one of these holds:

- b and c are the same text, after the path normalisation N below;
- b is `ffi` and c is `ffi:M`;
- b is `fs` and c is any `fs` grant;
- b is `fs:d` and c is `fs:d:P`;
- b is `fs:d:Q` and c is `fs:d:P`, and N(P) = N(Q), or - when neither
  holds a `\` - N(P) begins with N(Q) followed by `/`, or N(Q) is `.`
  and N(P) is relative and is neither `..` nor begins with `../`, or
  N(Q) is `/` and N(P) begins with `/`;
- b is `net` and c is any `net` grant;
- b is `net:H` or `net:H:p`, c is `net:h` or `net:h:q`, the port p is
  absent from b or equal to q (so a grant with a port does not cover
  one without), and either H and h are both wildcards and equal, or h
  is not a wildcard and H matches it (section 5.2);
- b and c are the same one of `io`, `env`, `clock`, `rand`.

N(P) is P with every run of `/` made one `/`; every `.` component
removed; every `..` removed together with the component before it,
when there is one and it is not `..`; a `..` directly after a leading
`/` removed; a trailing `/` removed; and an empty result made `.`. So
N(`./data/`) is `data`, N(`a/../b`) is `b`, and N(`../x`) is `../x`.
Comparison is case-sensitive. A path holding a `\` is covered only by
the same text or an unscoped grant, because on Windows `\` separates
components - `data/..\..\x` lies outside `data` - and on other systems
it does not (open question Q7).

This is the relation of section 5.5, applied grant by grant, with paths
compared as text instead of resolved.

### 9.6 The ratchet

A check derives every program of the tree (section 9.3) and compares
the result with the baseline B - **with B and nothing else**: not with
a previous commit, not with an earlier derivation. For each program P
that compiles, let E be B's entry for P's file, when there is one that
does not say `"compiles": false`. The tree widens B, and the check
fails, when any of these holds:

| | Widens when |
|---|---|
| W1 | a grant of P is not covered (section 9.5) by any grant of B's surface |
| W2 | P has a count for `fs` or `net`, B's surface has a grant of that effect, and P's count exceeds the surface's (`null` exceeds every number; a surface with no count for it has no bound) |
| W3 | there is an E, and a grant of P is not covered by any grant of E |
| W4 | there is an E with a grant of that effect, and P's count for `fs` or `net` exceeds E's |
| W5 | there is an E, P defines a function E's `functions` names, and P's declaration of it has an effect E's list for it does not |

Read by the kind of scope, a change widens B when it brings:

| Scope | A widening | Not a widening |
|---|---|---|
| an effect | a grant of an effect B's surface has no grant of | - |
| an `fs` path | `fs:d:P` with P outside every recorded path for d (`./data` widened to `./`); `fs:d` where B holds only paths for d; `fs` where B holds only `fs:read`/`fs:write` grants; any direction B does not hold | a path under a recorded one (`./data/x.csv` under `./data`); another spelling of the same path |
| a `net` host | a host no grant matches; `net:*.D` where B holds only single hosts under D; a grant without a port where B holds the host only with one; `net` where B holds only hosts | a host a recorded wildcard matches by one label; a host with a port where B holds it without one |
| an `ffi` module | a module B does not name; `ffi` where B holds only `ffi:M` grants | a module B names |
| a count | a larger number; `null` against a number | a smaller number or the same |
| a function | an effect added to a function B records, even when its program's grants and counts stay the same (W5) | a function B does not record; one that declares fewer effects |

These are **not** failures, and a check MUST NOT fail for them:

- **Narrowing**: a grant of B nothing needs, a lower count, a function
  that declares less. A check SHOULD report narrowing, so the baseline
  can be tightened.
- **A program B does not record.** It is held to W1 and W2 only: a new
  program that stays inside the surface the repository declared does
  not widen it.
- **A program B records that is not there**, or that does not compile
  now: one cannot run, and the other adds nothing until it compiles.
  A check SHOULD report both.
- **A different producer version** in B: a check SHOULD warn that its
  own derivation or standard library may differ from the producer's.

A check MUST report each widening: the grant, count or function, the
program, and which of W1 to W5 it fails - whether B's surface or the
program's own entry does not cover it. It SHOULD name the call that
makes a grant needed - file, line and function - and the chain of
calls from the program's `main` that reaches it, and the edit to B
that would accept the widening. The reference's `--json` report names
the rules in each finding's `rules`.

A check MUST NOT pass when it cannot compare: when there is no B, B is
not `sabline.capabilities/1`, or a grant in B is not one section 9.2
allows. The reference exits 2 in these cases, 1 for a widening, and 0
otherwise.

A tool MUST NOT write a baseline that does not cover the existing one,
unless a person asks for it in so many words - the reference's
`sabline capabilities init` refuses to replace a baseline without
`--force` - so that every widening arrives as a change to the file, in
review.

*Informative.* The reference's `sabline review --against REF` derives
the same for the files at a git ref, read with `git show` rather than
checked out, and reports how the working tree differs from it,
together with the proven share and the functions that became fallible.
It compares with a previous state, so it is a report for a reviewer,
not the ratchet: once a widening has been merged, a review against the
commit after it no longer sees it, and a check against B still does.

### 9.7 Example

[examples/sabline-lang.capabilities.json](examples/sabline-lang.capabilities.json)
is what sabline-lang 4.0.0 writes for a tree holding four of its
example programs. Each program's entry is the one sabline-lang's own
baseline holds for it; the surface is the union of these four alone:

```json
{
  "schema": "sabline.capabilities/1",
  "sabline_version": "4.0.0",
  "date": "2026-09-11",
  "surface": {
    "grants": ["clock", "env", "ffi:datetime", "ffi:math", "ffi:sqlite3",
               "fs:read", "fs:write:report.txt", "io",
               "net:raw.githubusercontent.com", "rand"],
    "counts": {"fs": 2, "net": 1}
  },
  "programs": [
    {"file": "examples/effects.vel",
     "grants": ["clock", "fs:read:report.txt", "fs:write:report.txt",
                "io", "rand"],
     "counts": {"fs": 2},
     "functions": {"dice": ["rand"],
                   "main": ["clock", "fs", "io", "rand"],
                   "save_report": ["fs"], "timestamp": ["clock"]}},
    {"file": "examples/pipeline.vel", "grants": ["io"], "counts": {},
     "functions": {"main": ["io"], "total_of": []}},
    ...
  ]
}
```

`fs:read:report.txt` is in `effects.vel`'s entry and not in the
surface, because `wordcount.vel` reads a path it is given, so the
surface holds `fs:read`, which covers it. If `pipeline.vel` came to
read a file named on its command line, it would need `fs:read`: the
surface covers that (W1 holds), but its own entry grants only `io`,
so W3 fails, and so does W5 for `main`. If `effects.vel` came to write
its report twice, its `fs` count would be 3: W2 and W4 fail.

### 9.8 What a baseline does not tell you

- **What a granted module does.** `ffi:os` in a baseline is the
  operating system, and a program that newly calls `os.system` through
  it is inside the surface (section 7).
- **Where a path leads.** Paths are compared as text; a symbolic link
  under a recorded directory is that directory's content. A budget
  built from the baseline resolves every path when it runs (section
  5.1), which is where that is caught.
- **A function's history.** A function is known by its file and name.
  One renamed as it gains an effect is a new function, held to W1 to
  W4 and not to what its old name declared.
- **Anything about a program that does not compile.**
- **Anything, if the check is not required.** A baseline is a control
  only where a failing check blocks a change, and an edit to the
  baseline is the acceptance of a widening: who may make that edit is
  the repository's decision.

## 10. Conformance

Conformance is defined by the conformance corpus in [tests/](tests),
not by this text. [CONFORMANCE.md](CONFORMANCE.md) defines three
levels - L1 Declaration, L2 Enforcement, L3 Ratchet - and names, for
each, the behaviours of sections 3 to 9 an implementation must have
and the cases that test them; [tests/README.md](tests/README.md) is
the contract for running the cases. The corpus is JSON, and runnable
by an implementation in any language that has never seen the
reference: 444 cases, 298 at L1, 37 at L2 and 109 at L3, 5 of them
recording the ratchet's known limits. No level requires a theorem
prover.

*Resolved in 0.4 (sabline-lang 4.1.0).* Versions 0.1 to 0.3 defined
conformance as passing six of the reference's own suites without the
prover - suites written against the reference's command line and
Python library, which an implementation in another language could run
only through an adapter (open question Q8). The corpus replaces that
definition. It is written from three of those suites' tables by
sabline-lang's `build_conformance.py`, and a drift test in both
repositories fails when the committed corpus is not what the suites
say. What it leaves out, and why, is in `tests/index.json` and
CONFORMANCE.md: the cases that depend on Python's object model, and a
few rules no case yet tests.

The table below is the reference's suites as they stand; they test the
reference, beyond the corpus.

| Suite | What it holds | Sections |
|---|---|---|
| `check_sandbox.py` | escape attempts against a budget given on the command line, each refused with the code it must carry (from 4.1): each effect refused; an effect hidden two helpers down; a refusal caught and carried on; the module list through `py`, `py_json`, `py_new` and a submodule path; the attribute-chain bound of section 5.3 - codecs through json, os.system through os, importlib to another module, a builtins type through a value, a `__globals__`/`__class__` traversal, a foreign object through a handle - with a deep attribute inside the granted module and a two-module grant still running; additive `fs`, `net` and `ffi`; a path outside a prefix, a write under a read grant, `..`, and a symbolic link (where the system will make one); a host outside the list, including a name when an address was granted; a port; a wildcard's parent domain; redirects to a granted and to an ungranted host; counts on `fs` and `net`; `env` under `io`; and from 4.1 `@0`, a count spent by an operation that then fails, a URL with no scheme taken as HTTPS, and an existence check under a write grant. The corpus's level 2 is written from it | 4, 5, 6 |
| `check_library.py` | the same through the reference's library, its HTTP door's ceiling (section 5.5) and its MCP server; that the library and the server report the same audit; that `safe_command` round-trips for awkward paths and hosts (section 8.3); that every malformed budget raises a readable budget error and never a traceback (section 4.2); from 4.1, 55 budgets each held to the grants sections 4 and 5 give it, or to its refusal, and 18 programs each audited to the effect surface section 8 gives it; that the command line's `audit --json` is `sabline.audit/1` and validates against the schema (section 8); from 4.2, that a Statement `sabline attest` writes validates against in-toto's Statement v1 schema, the predicate's and the audit's, that its audit is `audit()`'s for the same program field for field, that a directory gives one Statement per file, that each digest is the sha256 of the file's bytes, and that a module named while running is carried as `ffi_any` (section 8.5). The corpus's level 1 is written from its tables | 3.2, 4, 5, 6, 8 |
| `check_refusals.py` | wrong programs refused with the right code, among them an undeclared effect (E300) | 3.2 |
| `check_fallible.py` | every fallible builtin refused when its failure is ignored, and its failure catchable - the redirect failure of G4 among them | 6, 8 |
| `check_termination.py` | the termination verdict for each of 44 adversarial loops, which `sabline.audit/1` reports as `loops_unshown` | 8 |
| `check_ratchet.py` | the comparison of section 9.6, through the reference's command line, in scratch trees and real git histories: a six-commit history whose sixth commit reaches a new host three calls down, failing at that commit only, with the file, function, line and call chain named; a widening merged once and still failing against the baseline at every later commit, where a comparison with the previous commit reports nothing; widenings through an import, the standard library, a path prefix, a count, a wildcard host, a URL, path or module built while running, a new module, a new direction, and a program whose `main` is imported from outside the tree; an effect added to a function while its program's grants stay the same (W5); and changes that must pass - narrowing, reordering and reformatting, a file with no effects, a new program inside the surface, a literal moved into a variable, a function renamed or moved; the covering relation (9.5) and the operation bound (9.4) case by case; a baseline from another version (a warning), and baselines that cannot be read (exit 2); from 4.1, the baseline written for each of 14 trees, the writer refusing to replace a baseline unasked, and the five known limits of 9.8, each with the outcome the reference gives. The corpus's level 3 is written from its tables | 9 |

Neither the suites nor the corpus test every rule stated here;
CONFORMANCE.md lists the rules no case tests. Passing the corpus is
evidence about the cases it holds, and no more.

## 11. Open questions

Each question is a point where this document records the reference's
behaviour, or where the reference's own text and behaviour disagree,
without settling what is right. Q1, Q2, Q3, Q5 and Q6 were open in
version 0.1 and are **resolved in 0.2** (sabline-lang 3.3.0); Q4 is
**resolved in 0.3** (sabline-lang 4.0.0); Q8, Q9 and Q11 are
**resolved in 0.4** (sabline-lang 4.1.0), and the part of Q11 that 0.4
left to the reference is done in 0.5 (sabline-lang 4.2.0). They are
kept here, marked resolved, so the record of what changed stays with
the question.

- **Q1. Unknown names in declarations. Resolved in 0.2.** Version 0.1
  asked whether a checker should reject a `uses` name that is not one of
  the seven. From sabline-lang 3.3.0 it does, with E300 naming the
  seven; from 4.1.0 the audit reporting that E300 lists only the seven
  too, so `sabline.audit/1`'s `effects` is always a subset of them
  (section 3.2, resolved in 0.4).
- **Q2. "Grants are additive" and `ffi`. Resolved in 0.2.** Version 0.1
  followed the parser, which restricted `ffi` to the named modules when
  both `ffi` and `ffi:M` appeared, against the reference text's "Grants
  are additive". From sabline-lang 3.3.0 `ffi` is additive like `fs` and
  `net` - the wider grant wins - so text and parser agree (section 4.3).
- **Q3. The command line's audit. Resolved in 0.2.** Version 0.1
  recorded that `sabline audit FILE --json` printed a shape that is not
  `sabline.audit/1`. From sabline-lang 3.3.0 it prints
  `audit().as_dict()`, the same document as every other door (section 8).
- **Q4. No flag for a computed module name. Resolved in 0.3.** Version
  0.2 recorded that `sabline.audit/1` had `read_any`, `write_any` and
  `any`, and nothing for `ffi`. From sabline-lang 4.0.0 it has `ffi_any`,
  added within version 1 (section 8.2), and section 9 takes a program
  whose `ffi_any` is true to need unscoped `ffi`.
- **Q5. `safe_command` for IPv6 hosts and awkward paths. Resolved in
  0.2.** Version 0.1 recorded the unbracketed IPv6 form and the paths
  that did not round-trip. From sabline-lang 3.3.0 IPv6 hosts are
  bracketed in the grammar, in `net_hosts` and in `safe_command`, and
  `, @ [ ] %` are percent-encoded in paths and hosts (sections 5.1, 5.2,
  8.3), so `safe_command` round-trips. Changing `net_hosts` to bracket
  IPv6 is a change to what that field contains; it is made here in a new
  format version, not within version 1 silently.
- **Q6. Stray forms the parser accepts. Resolved in 0.2.** Version 0.1
  recorded a count with non-ASCII digits, `ffi:M@N`, and `ffi:` with no
  module. From sabline-lang 3.3.0 each is a budget error (sections 4.2,
  5.3), and no malformed budget produces a traceback.
- **Q7. Windows paths in baselines.** Section 9.5 compares paths as
  text with `/` as the only separator, and case-sensitively. A program
  written for Windows may name `data\in.csv`; two spellings of one path
  then compare as different, and the check fails rather than passes -
  the safe direction, but noisy. From 0.3 a path holding a `\` is
  covered only by the same text or an unscoped grant, because on
  Windows `data/..\..\x` lies outside `data`: the version 0.2 rule
  would have let a recorded prefix cover it. Whether a baseline should
  instead normalise `\` on every platform is still open.
- **Q8. A conformance harness for other languages. Resolved in 0.4.**
  Versions 0.1 to 0.3 defined conformance by suites that drive the
  reference's command line and Python library. From 0.4 conformance is
  the corpus in `tests/`, JSON cases with a runner contract
  (`tests/README.md`), at three levels (CONFORMANCE.md), which an
  implementation in any language runs its own way (section 10).
- **Q9. Rules stated here and not yet tested by the suite. Resolved in
  0.4.** From sabline-lang 3.3.0 the suite covers a function argument
  that is a dotted path through a granted module's attributes (section
  5.3), `ffi` together with `ffi:M` (section 4.3), and IPv6 grants
  bracketed and not (section 5.2). From 4.1.0 it covers the four 0.3
  listed as untested - a URL without a scheme taken as HTTPS (5.2), an
  existence check under a write-only grant (5.1), `@0`, and a count
  spent by an operation that then fails (5.4) - and each is a case of
  the corpus. The rules still without a case are listed in
  CONFORMANCE.md, and belong there rather than here.
- **Q10. The reference text's table.** Its row `...@N` reads as if a
  count could follow any grant; the reference accepts counts only on
  `fs` and `net` (section 4.2).
- **Q11. Attestation. Resolved in 0.4.** Version 0.3 recorded that
  `sabline.audit/1` is unsigned and names no artifact digest. Section
  8.5 defines an in-toto predicate type,
  `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`,
  that carries an audit with the digests of the files audited, so a
  signed Statement can say which source it describes. From
  sabline-lang 4.2.0 the reference writes Statements of it too
  (`sabline attest`, section 8.5), and signs none. From 0.11.0 the type
  is named `https://velaris-lang.dev/capability/v1`, and the name above is
  accepted for verification (section 8.5).

## Appendix A. The reference binding

Informative: which builtins of sabline-lang 4.2.1 perform which
operations. They are unchanged since 3.3.0.

| Builtins | Effect | Operation | Checked beyond the effect |
|---|---|---|---|
| `print`, `log`, `ask`, `read_line`, `args`, `exit_with` | `io` | the console | nothing |
| `env` | `env` | read an environment variable | nothing |
| `read_file` | `fs` | read; path is the first argument | path (5.1), count (5.4) |
| `write_file` | `fs` | write; path is the first argument | path, count |
| `file_exists` | `fs` | existence; path is the first argument | path (read or write grant), count |
| `fetch`, `post`, `fetch_status` | `net` | request; URL is the first argument | host and port (5.2), count, redirects |
| `request` | `net` | request; URL is the second argument | host and port, count, redirects |
| `now` | `clock` | read the time | nothing |
| `random` | `rand` | draw a number | nothing |
| `py`, `py_int`, `py_float`, `py_json`, `py_new` | `ffi` | call into Python; module is the first argument | the module named and every module reached along the attribute chain the call names (5.3) |
| `py_do`, `py_field` | `ffi` | use a host object already held | the module owning the method or field reached, and a foreign object returned (5.3) |
| `py_close` | `ffi` | release a held object | nothing |

The reference's standard library modules (`http.vel`, `db.vel`,
`time.vel`, `dates.vel`, `env_tools.vel`, `log.vel` and others) are
written in Sabline, and carry the effects of the builtins they call
through their declarations: a program using `http.vel` declares `net`,
one using `db.vel` declares `ffi`.

## Appendix B. Codes

| Code | When | The program can handle it | What the reference library reports as refused |
|---|---|---|---|
| E310 | an operation's effect is not granted | no | the effect, e.g. `fs` |
| E311 | a module outside the `ffi:` grants | no | `ffi:` and the module as the call gave it |
| E313 | a path outside the `fs:` grants | no | `fs:` and the path as the program gave it |
| E314 | a host or port outside the `net:` grants, or a URL with no host or an unreadable port | no | `net:` and the host |
| E315 | a count reached | no | `fs@count` or `net@count` |
| - | a redirect to a target outside the grants (G4) | yes: an ordinary failure naming the target | nothing |

Compile-time codes for the static rule: E300 (T1 and T2), E530 (T4),
E310 (T5).

The reference's `Secret of T` (sabline-lang SPEC.md section 3.1, and
section 8.6 here) adds four compile-time codes of its own. They are
not part of the static rule this document specifies, and an
implementation without such a type gives none of them: E560, a value
that must not escape given to something that emits it or to something
that can fail; E561, a `declassify` without a reason written in the
call, or given something that is not one; E562, a Secret of a Secret;
E563 (sabline-lang 7.0.0), an `if` or `while` branching on a value
derived from one.

The reference's version 8.0.0 adds three more codes of its own, none
part of the static rule this document specifies, and an implementation
need not give them: **E204**, a function named like a built-in, which
the reference refuses rather than shadow (its SPEC.md 10.1); **E317**, a
network request whose socket peer is a proxy the run's `net` grants do
not cover (an ambient `HTTP_PROXY`/`HTTPS_PROXY`); and **E318**, a
`read_file` of a documented credential location, pointed at the
reference's `read_file_secret`. E317 tightens the reference's
enforcement of section 6 G4/G5 to the socket's peer, not only the URL;
E318 is a reference policy over which files a plain read may touch.

The reference's version 8.1.0 adds three more of its own, none part of
the static rule: **E515**, an import from outside the directory a program
is served from, or of a file there that is not a `.vel` file - its HTTP
door and MCP server hold a program's imports to the directory they serve;
and **E613** and **E614**, a check or an audit that ran past its time or
its memory ceiling and was stopped, so that source written to stall the
checker is answered rather than waited on. A `sabline.audit/1` document
reporting E613 or E614 has `ok` false and determines nothing (section
8.4).

The reference's version 8.3.0 adds two more of its own, neither part of the
static rule: **E615**, a run under its evaluation profile (section 8.9) asked
to stop from outside, which stopped at the next call or loop turn or had its
worker killed; and **E616**, a run the reference replayed with recorded tool
responses that made a call the recording does not hold in that place.

The reference's version 8.5.0 adds five for the `tool` effect, none of
which a program can handle: **E320**, a call with no tool to reach - the
run was given no manifest, or the manifest does not offer the tool;
**E321**, a tool or an argument outside the tool grants (section 5.6);
**E322**, a count or the manifest's ceiling passed; **E323**, arguments the
tool's schema does not accept, or a secret result asked for as an ordinary
one; and **E324**, a host that did not keep the reference's exchange.

The reference's version 8.4.0 adds **E319**: an effect its own runtime
attempted outside the budget, refused by the operating system's confinement.
It is given only under the reference's fault-injection hook, which exists so
its suites can show the kernel refusing; no program reaches it.

## Appendix C. Changes

- **0.13.0**, 2026-09-20: tracks sabline-lang 8.5.0. A ninth effect,
  `tool` (sections 3.1, 4.1, 5.6), with a provisional manifest of tools
  (8.10); `hmac_sha256` and `hmac_sha256_chain` as operations of
  `declassify`, named in the audit's `secrets` with the reason `hmac
  signature` (8.6); `tools` in the audit and the host of a URL that begins
  fixed in `net_hosts` and in a baseline's grants (8.2, 9.3); and in a
  receipt `grants_used`, `key_fingerprint`, `tool_calls` and `tool_ceiling`
  (8.7). Everything valid under 0.12.0 is valid and means the same; the
  corpus is unchanged, and cases for `tool` will join it when 8.10 stops
  being provisional. The quoted reference text (section 2) is 8.5.0's.
- **0.12.0**, 2026-09-19: tracks sabline-lang 8.4.0, which asks the
  operating system to hold a run's budget. **8.7**: `run_parameters.
  confinement` is a level - `full`, `partial`, `none` - and gains
  `confinement_reason`, `confinement_layers` and `os_policy_sha256`, all
  optional, within version 1. **8.2**: `sabline.audit/1` gains `confinement`,
  the level on each of three systems for a run under `safe_command` and the
  Python modules that widen it, within version 1. **8.9**: a producer that
  writes the evaluation profile's name must not have run at `none`, and the
  mechanism names move to `confinement_layers`. **Appendix B** lists the
  reference's E319. No rule of sections 3 to 7 or 9 changes, no conformance
  case changes, and section 2 still quotes sabline-lang SPEC.md sections 6,
  7 and 7.1 word for word.
- **0.11.0**, 2026-09-15: tracks sabline-lang 8.3.0. **8.5 and 8.7**: the
  predicate types are named at sabline.dev, a domain the reference's
  project holds; their earlier names, on the reference's GitHub Pages
  address, are accepted for verification, and a producer writes the new
  ones. `velaris.dev` names no type of this document. **8.7**: a receipt
  gains `stop` and `run_parameters.profile` within version 1, and both
  schemas name the new types. **8.8 is new**: what a receipt compared with
  an audit, and with earlier receipts of the same subjects, can name as a
  difference, and the reference's provisional `sabline.receipts-diff/1`.
  **8.9 is new**: what a receipt of a run under an evaluation profile
  asserts, the confinement words the reference writes, and `stop`.
  **Appendix B** lists the reference's E615 and E616. No rule of sections 3
  to 7 or 9 changes, no conformance case changes, and section 2 still quotes
  sabline-lang SPEC.md sections 6, 7 and 7.1 word for word.
- **0.10.0**, 2026-09-14: tracks sabline-lang 8.1.0. **8.7 is new**:
  `sabline.receipt/1`, a record of one run - the budget, each refusal and
  declassification, the parameters, how the run ended and how long it
  took - and the in-toto predicate type `.../receipt/v1` that carries it,
  bound by digest to the subjects a Statement of 8.5 names. A receipt MUST
  NOT hold a value the program handled, and 8.7 says what it still does
  not hide: what a program controls that is not a value. Its schema is
  `schemas/receipt-predicate.v1.schema.json`, and `tools/check_sync.py`
  holds it to the copy the reference publishes. **Appendix B** lists the
  reference's E515, E613 and E614. No rule of sections 3 to 7 or 9
  changes, no conformance case changes, and section 2 still quotes
  sabline-lang SPEC.md sections 6, 7 and 7.1 word for word.
- **0.9.0**, 2026-09-14: tracks sabline-lang 8.0.0. No rule of this
  format changes. `sabline.audit/1` gains one field within version 1
  (section 8.2, 8.1's compatibility rule): `ffi_native`, per named
  Python module whether native code ships with it, decided from files on
  disk without importing the module - `"native"` or `"unknown"`, never
  `"false"`. It reflects the producing machine's installed packages, so
  it is not reproducible across machines, and an attestation embedding it
  (section 8.5) says only what that machine found. A producer without
  the notion writes it empty or omits it, and a consumer ignores a field
  it does not know (section 8.1). 8.0.0's breaking changes are in the
  reference's runtime and error codes (Appendix B adds E204, E317, E318),
  not in this format, so no conformance case changes and the corpus is
  unchanged. Section 2 still quotes sabline-lang SPEC.md sections 6, 7
  and 7.1 word for word - those sections did not change in 8.0 - so
  `tools/check_sync.py` still passes.
- **0.8.0**, 2026-09-12: tracks sabline-lang 7.0.0. No rule of this
  format changes: `declassify` is still the eighth effect and `secrets`
  still holds the same three fields. What changed is in the reference's
  type system, and two places here describe it. **8.6** said the rule
  behind `secrets` bounds explicit flow only, and that a program with
  `declassifies: false` could still tell a reader about a secret
  through its own control flow. That was true of sabline-lang 6.0.0,
  where a comparison over such a value gave an ordinary boolean, and it
  was a hole: with a length and a character read, a comparison in a
  loop reads the whole value out. 7.0.0 makes a comparison give another
  protected value and refuses any branch on one (E563), so the bullet
  is narrowed to what remains - that this is not a non-interference
  result, and says nothing about how long a program runs or whether it
  stops. **Appendix B** lists E563 with the other three. A producer
  with no such type system is unaffected by either.
- **0.7.0**, 2026-09-12: tracks sabline-lang 6.0.0, which added
  `Secret of T` - a value the type system will not let a program emit.
  Two things follow for this format. **3.1** gains an eighth effect,
  `declassify`, the one operation that removes the mark: it reaches
  nothing outside the program, but it is declared, propagated and
  refused exactly as the other seven are, so nothing in sections 4 to 7
  treats it specially and a budget naming it parses everywhere. An
  implementation with no such type system has no operation covered by
  it. **8.6** is new: `sabline.audit/1` gains a `secrets` object -
  which builtins handed the program such a value, whether it ever
  declassifies one, and with what stated reasons - so that a consumer
  can ask whether a program lets a secret out without running it. It is
  an added field within version 1, and a consumer that does not know it
  ignores it. What it does not claim is written there: the reasons are
  unchecked text, the rule bounds explicit flow only, and it covers
  only the values those builtins produced. The corpus grows from 444
  cases to 455: eight L1 cases for the new field and the refusals
  around it, three L2 cases for the grant, and one L2 case reworded
  because the program it held no longer compiles.
- **0.6.0**, 2026-09-12: tracks sabline-lang 5.0.0, which made `io` the
  budget a run gets when nobody writes one. Two sections are restated.
  **4.6** said the reference's command line and library grant all seven
  effects, unscoped, when given no budget; from 5.0 they grant `io`,
  and so do the worker pool and both doors, so every place a budget
  comes from in the reference now answers the same way. The SHOULD for
  other implementations is unchanged, and what a runtime does with no
  budget is still outside this format. **4.4** said that when no grants
  are given a denial starts from all seven effects; it now says a
  denial narrows the runtime's default budget, which this format does
  not fix, and that a conformance case always writes the grants its
  denial applies to. One case changes with it:
  `L1-budget-deny-from-all-seven` becomes
  `L1-budget-deny-from-grants-given`, which grants the seven in its
  own text and denies two of them, and a case asserting the reference's
  new default is recorded in `tests/index.json` as excluded rather than
  required of everyone. The corpus is still 444 cases. `--allow all`,
  the reference's shorthand for the seven effects, is an operator's
  command-line word and not part of the grammar of sections 4 and 5: a
  budget a caller sends over a door still cannot contain it.
- **0.5.3**, 2026-09-12: tracks sabline-lang 4.3.2. No rule, field,
  schema or case changes; the corpus is still 444 cases. sabline-lang
  4.3.0 added `Money of CUR` and 4.3.1 made a proof that runs out of
  time say so; neither touches the capability format, so this version
  moves only the reference's version number and the documents that
  name it.
- **0.5.2**, 2026-09-11: tracks sabline-lang 4.2.1. No rule, field,
  schema or case changes. Two drafts, not sent, sit beside the
  specification: MCP_PROPOSAL.md, a capability declaration for Model
  Context Protocol tools in the grammar of sections 4 and 5, and
  NIST_SUBMISSION.md, input to NIST's AI Agent Standards Initiative.
  REGISTRY_SUBMISSION.md records that the in-toto pull request's branch
  is pushed and what is left before it is opened.
- **0.5.1**, 2026-09-11: tracks sabline-lang 4.2.1. No rule, field,
  schema or case changes. The author's name is written with a capital
  S - Palakurthi Gowri Shankar, given name Gowri Shankar - in
  CITATION.cff, NOTICE, README.md, PROVENANCE.md and
  REGISTRY_SUBMISSION.md. The schemas' `$id` values still point at the
  `v0.5` tag, whose schemas are these.
- **0.5**, 2026-09-11: tracks sabline-lang 4.2.0, which writes the
  Statements of section 8.5 (`sabline attest`). `sabline.audit/1` gains
  two optional fields within version 1 (section 8.2): `counts`, the
  bound of section 9.4 on `fs` and `net` operations, `null` where none
  is determined; and `prover`, whether a prover decided the promises'
  status. Section 8.4 says what a count is not. Section 8.5 records the
  producer, and `examples/capability-statement.json` is now what it
  writes rather than a Statement assembled by hand. The predicate type,
  its URI and its schema are unchanged. The corpus is unchanged: 444
  cases. Section 2 still quotes sabline-lang SPEC.md sections 6, 7 and
  7.1 word for word - those sections did not change in 4.2 - so
  `tools/check_sync.py` still passes.
- **0.4**, 2026-09-11: tracks sabline-lang 4.1.0. Conformance is a
  corpus any implementation can run: `tests/`, 444 JSON cases written
  from three of the reference's suites and held to them by a drift test,
  with a runner contract (`tests/README.md`) and three levels, L1
  Declaration, L2 Enforcement and L3 Ratchet (CONFORMANCE.md); section
  10 is rewritten around it, and Q8 and Q9 are resolved. Section 8.5
  defines an in-toto predicate type for `sabline.audit/1`, resolving
  Q11. Sections 3.2, 8.2 and 8.3 are corrected: they said an audit's
  `effects` is always a subset of the seven and its `safe_command`
  always parses, which was false, until sabline-lang 4.1.0, for the
  audit of a program refused for naming an unknown effect. Section 2
  still quotes sabline-lang SPEC.md sections 6, 7 and 7.1 word for word -
  those sections did not change in 4.1 - so `tools/check_sync.py` still
  passes.
- **0.3**, 2026-09-11: tracks sabline-lang 4.0.0, which reads and writes
  baselines. Section 9 is no longer provisional: `sabline.capabilities/0`
  is replaced by `sabline.capabilities/1`, which records the
  repository's surface as well as each program's grants, a bound on
  `fs` and `net` operations (9.4), each function's effects, and the
  producer's version and date; the derivation (9.3) reads fixed text,
  not only literals, and takes an imported `main` into account; the
  covering rule (9.5) compares a path holding `\` whole; and the
  comparison (9.6) is stated as five rules, W1 to W5, with a table of
  what widens for each kind of scope, and the rule that a check
  compares with the baseline and nothing else. Resolves Q4:
  `sabline.audit/1` gains `ffi_any` (section 8.2). Section 4.6 records
  that the reference's HTTP door has had an `io` ceiling by default
  since 4.0; section 10 adds `check_ratchet.py` to the conformance
  suite. Section 2 still quotes sabline-lang SPEC.md sections 6, 7 and
  7.1 word for word - those sections did not change in 4.0 - so
  `tools/check_sync.py` still passes.
- **0.2**, 2026-09-11: tracks sabline-lang 3.3.0, which fixed the five
  defects the 0.1 extraction found. Resolves Q1 (an unknown name in a
  `uses` clause is rejected, section 3.2), Q2 (`ffi` grants are additive;
  the wider grant wins, section 4.3), Q3 (the command line's
  `audit --json` emits `sabline.audit/1`, section 8), Q5 (`safe_command`
  and `net_hosts` bracket IPv6, and the escaping rule holds `,`, `@` and
  the rest in paths and hosts, sections 5.1, 5.2, 8.3, 8.4), and Q6
  (a non-ASCII count digit, `ffi:M@N` and `ffi:` with no module are
  budget errors, sections 4.2, 5.3). Adds the percent-encoding escaping
  rule to sections 5.1 and 5.2. Notes in Q9 the rules the suite now
  covers. Section 2 still quotes sabline-lang SPEC.md sections 6, 7 and
  7.1 word for word - those sections did not change - so
  `tools/check_sync.py` still passes.
- **0.1**, 2026-09-11: first version, extracted from sabline-lang
  3.1.1.
