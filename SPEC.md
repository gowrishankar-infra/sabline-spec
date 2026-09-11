# The Velaris capability format

Version 0.2, 2026-09-11. Dedicated to the public domain under CC0 1.0;
see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Reference implementation: velaris-lang,
<https://github.com/gowrishankar-infra/velaris-lang>. This text was
first extracted from velaris-lang 3.1.1 (commit `25d2c05`); version 0.2
tracks velaris-lang 3.3.0, which fixed the five defects the extraction
found, and describes what that version does. Conformance is defined by
the suite in that repository (section 10), not by this text.

## 0. About this document

This document specifies:

- the seven effects a Velaris program can declare, and the rule that
  makes a function's declaration cover everything a call to it can
  reach (section 3);
- the grammar an operator uses to grant effects, narrowed to paths,
  hosts, ports, Python modules and operation counts (sections 4 and 5);
- what a runtime enforcing a grant must refuse, and when (section 6),
  and what a grant does not bound (section 7);
- `velaris.audit/1`, the JSON report of what a program declares and
  names (section 8);
- `velaris.capabilities/0`, a provisional JSON baseline a repository
  can hold its programs to (section 9).

It does not specify the rest of the Velaris language - types,
contracts, proofs, failure - or the time and memory limits a runtime
may also impose, or any command line or library interface beyond what
is needed to state the above. The reference implementation's own
SPEC.md, EMBEDDING.md and THREAT_MODEL.md cover those.

**Conventions.** MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be
read as described in RFC 2119 and RFC 8174 when, and only when, they
appear in capitals. "The reference" means velaris-lang 3.3.0. A
paragraph marked *Reference behaviour* records what the reference does
at a point this document does not yet settle; each such point is also
an open question in section 11. A paragraph marked *Resolved in 0.2*
records a point that version 0.1 left open and this version settles,
naming the velaris-lang release that made the reference match.

Where this document and the reference disagree, that is a bug in one of
them. Until it is resolved, the conformance suite decides.

## 1. Terms

| Term | Meaning |
|---|---|
| program | one or more `.vel` files: an entry file and what it imports |
| operator | whoever runs a program and chooses its budget |
| effect | one of the seven names in section 3.1 |
| declaration | a function's `uses` clause |
| budget | the grants an operator gives a run |
| grant | one item of a budget (section 4) |
| operation | one attempt by a running program to do something an effect covers - one file read, one request, one call into Python (section 3.1) |
| run | one execution of one program, from its start to its end |
| refusal | the runtime ending a run because an operation lies outside the budget (section 6) |
| producer, consumer | a program that writes, or reads, a document defined here |

## 2. The reference text

The three sections below are copied without change from velaris-lang
SPEC.md sections 6, 7 and 7.1 - the reference's own language
specification. They are the normative core of this document. Sections
3 to 7 state the same rules precisely enough to implement without
reading the reference's source, and say where the reference does
something this text does not.

`tools/check_sync.py` compares each block with velaris-lang SPEC.md and
fails if a word differs; this repository's CI runs it on every push and
every week. A change to those sections in velaris-lang is a change this
document must follow.

Section numbers inside the quoted text (such as "§8" and "§12") refer to
velaris-lang SPEC.md, not to this document.

### 2.1 Evaluation (velaris-lang SPEC.md section 6)

<!-- verbatim: velaris-lang SPEC.md "## 6. Evaluation" -->
Evaluation is strict, left to right, depth first. Arguments are fully
evaluated before a call. `and` and `or` short-circuit: the right side
is not evaluated when the left decides the result. `if`/`while`
conditions must be `Bool`; there is no truthiness.

There is no undefined behaviour. Every operation either produces a
value, raises a language error with a code, or fails in the sense of
§8.
<!-- end verbatim -->

### 2.2 Effects (velaris-lang SPEC.md section 7)

<!-- verbatim: velaris-lang SPEC.md "## 7. Effects" -->
A function declares what it may do:

    fn save(path: Text, body: Text) uses fs { ... }

The effects are `io` (the console: `print`, `read_line`, `args`),
`env` (environment variables, through `env()`), `fs` (files), `net`
(network), `clock` (the time), `rand` (randomness) and `ffi` (calling
the host language, §12). `env` became its own effect in 3.0; before
that it was part of `io`, which meant an io-only budget could read
every secret in the environment.

The rule is transitive and checked at compile time: a function may
only perform effects it declares, and calling a function requires
declaring everything that function declares. A function with no `uses`
clause is **pure** — it cannot perform any effect, and neither can
anything it calls, however deep. Violations are E300.

This is a property of the whole call graph, not a convention. Reading
a signature tells you the complete set of things a call can do to the
outside world.
<!-- end verbatim -->

### 2.3 The budget (velaris-lang SPEC.md section 7.1)

<!-- verbatim: velaris-lang SPEC.md "### 7.1 The budget" -->
Declaring an effect is the program's claim; the **budget** is the
operator's decision, given as `--allow` / `--deny` on the command line
or `allow=` in the library, and enforced by the runtime at the moment
an effect is attempted, whatever the source declares. A refusal stops
the program and cannot be caught.

A grant names an effect, and may narrow it:

| Grant | Permits |
|---|---|
| `io`, `env`, `clock`, `rand` | that effect |
| `fs` | any path, read and write |
| `fs:read`, `fs:write` | one direction, any path |
| `fs:read:P`, `fs:write:P` | one direction, for paths that resolve under `P` |
| `net` | any host |
| `net:H`, `net:H:PORT` | that host, at any port or at that port |
| `net:*.D` | hosts with exactly one label in place of the star |
| `ffi` | any Python module |
| `ffi:a,b` | those top-level modules |
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

### 3.1 The seven effects

| Effect | Covers | Operations in the reference (Appendix A) |
|---|---|---|
| `io` | the console: standard output, standard error, standard input, the program's command-line arguments, its exit status | `print`, `log`, `ask`, `read_line`, `args`, `exit_with` |
| `env` | reading environment variables | `env` |
| `fs` | the file system: reading a file, writing a file, asking whether a path exists | `read_file` (read), `write_file` (write), `file_exists` (existence) |
| `net` | the network: one HTTP or HTTPS request | `fetch`, `post`, `fetch_status`, `request` |
| `clock` | reading the current time | `now` |
| `rand` | drawing a random number | `random` |
| `ffi` | calling into the host language - Python, in the reference - and using host objects | `py`, `py_int`, `py_float`, `py_json`, `py_new`, `py_do`, `py_field`, `py_close` |

Effect names are lower case and matched exactly. The list is closed in
this version; a new effect is a new version of this document. The
reference text's list for `io` ("`print`, `read_line`, `args`") names
examples; the table above is the complete list for the reference.

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

A `uses` clause names effects, and the seven are the only ones. A
conforming checker MUST reject a `uses` clause naming anything else,
before running the program, naming the seven.

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that the
reference accepted any identifier in a `uses` clause: `uses io, teleport`
compiled, `velaris.audit/1` listed `teleport` among the effects, and the
audit's `safe_command` became a budget that does not parse. From 3.3.0
the reference rejects an unknown name with E300, naming the seven, so
`velaris.audit/1`'s `effects` is always a subset of them. This closes
open question Q1.

## 4. The grant grammar

A budget is written as text: grants separated by commas, such as
`io,fs:read:./data,net:api.example.com:443@100`.

### 4.1 Forms

| Form | Grants |
|---|---|
| `io`, `env`, `clock`, `rand` | that effect |
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
      contains neither `:` nor `@`, and is not one of the seven effect
      names, add it as another module and move past it. So `ffi:math,json`
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

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that the
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

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded the reverse:
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
When no grants are given, the starting budget is all seven effects,
unscoped. Each denied name MUST be one of the seven effects; it removes
the effect with its scope and count. A denial cannot be scoped:
`--deny fs:write` is an error.

### 4.5 A budget given as a list

Some interfaces take a budget as a list of strings. Each element SHOULD
be one complete item, and each module SHOULD be written as its own
`ffi:M`, because the continuation form of step 2.2 depends on order.
The reference library sorts the list and joins it with commas before
parsing, so `["ffi:math", "json", "io"]` becomes `ffi:math,io,json`, an
error; the reference HTTP door joins its list in no defined order.

### 4.6 When no budget is given

This format defines what a budget grants. It does not define what a
runtime does when the operator gives no budget at all. The reference
command line (`velaris file.vel`) and library (`velaris.run(source)`
with no `allow`) then grant all seven effects, unscoped. What makes a
run deny-by-default is the budget, not the program or the format. The
reference's MCP tool `velaris_run` and its HTTP `POST /run` default to
`io` alone. A tool built on this format SHOULD require an explicit
budget, or default to one that grants no more than `io`.

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

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that the
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

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that the
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

### 5.5 One budget inside another

The reference uses this relation for its HTTP door's ceiling
(`--max-allow`): a request may ask for any budget the ceiling covers.
Section 9 uses it, grant by grant, for baselines. A budget C covers a
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
  system as the current user. From velaris-lang 3.3.0 an `ffi:M` grant
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
  and a memory cap as settings of a run. They are not part of this
  format, and they have platform limits of their own (see the
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

## 8. velaris.audit/1

`velaris.audit/1` is a JSON object that describes a program before it
runs: what it declares, what it names, what it promises, and whether
each promise is proven. In the reference it is what
`velaris.audit(source).as_dict()` returns, and what the reference's MCP
tool `velaris_audit`, the `POST /audit` endpoint of its HTTP door, its
npm `audit()`, its CrewAI audit tool, its GitHub Action's pull request
comment, and - from velaris-lang 3.3.0 - its command line's
`audit --json` are built on. Its JSON Schema is
[schemas/velaris.audit.1.schema.json](schemas/velaris.audit.1.schema.json);
[examples/audits/](examples/audits) holds four documents the reference
produced.

*Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that the
command line was the exception: in velaris-lang 3.1.1 `velaris audit
FILE --json` printed an older, unversioned summary with different fields
- `file`, `compiles`, `errors`, `effects`, `functions` as a count,
`proven`, `checked_at_runtime`, `reaching_outside`, `can_fail`,
`loops_unshown` as an object, `contract_coverage`, and a `safe_command`
built from the coarse effects alone - which the schema rejected because
it has no `schema` field. From 3.3.0 the command line prints
`velaris.audit(source).as_dict()`, the same document as every other
door, and its `safe_command` is derived as section 8.3 says (so
`examples/json_ffi.vel` gives `ffi:math,io`, not `ffi,io`). This closes
open question Q3.

### 8.1 Compatibility

Within version 1, fields may be added. No field changes meaning or
disappears without the `schema` value changing. A consumer MUST ignore
fields it does not know. Fields added after version 1 was first
released (in velaris-lang 2.52) are optional in the schema, because
documents from earlier producers lack them; the table says when each
was added.

### 8.2 Fields

| Field | Type | Meaning | Added |
|---|---|---|---|
| `schema` | string | `"velaris.audit/1"` | |
| `velaris_version` | string | the version of the producer | |
| `ok` | boolean | true when the program compiled: it parsed, and the checks the reference makes before running - of `main`, effects, types and proofs - reported no problem. A file with no `main` is audited as a library and is not a problem. A proof that a promise is false (E700) makes `ok` false. | |
| `problems` | array | one object per problem: `code` (`E` and three digits), `message`, `line` (integer), `file`, `fixes` (array of strings). Empty when `ok` is true. | |
| `effects` | array of strings | the union of the declarations of every function defined in the audited file, sorted, without repeats. Through the transitive rule it includes everything those functions can reach in imported files. When `ok` is true, it is an upper bound on the effects a run can attempt. When `ok` is false it is whatever could be read - not a bound - and may be empty. | |
| `functions` | array | one object per function defined in the audited file, in source order (inline function values are not listed): `name`; `effects`, its own declaration, sorted; `can_fail`, true when declared `or fail`; `requires` and `ensures`, each contract expression as text; `status`; `loops_unshown` (integer, added 2.62). | |
| `functions[].status` | string | `"proven"`: every promise was proven before running, which happens only when a prover ran. `"checked at runtime"`: it has promises, not all proven. `"no promises"`: no `requires` or `ensures`. `"error"`: a problem was reported on the function's line. | |
| `proven_share` | number or null | 100 × (functions with a promise whose status is `"proven"`) ÷ (functions with at least one `requires` or `ensures`), rounded to one decimal place; null when no function has one | |
| `safe_command` | string | `velaris <file> --allow G`, where `<file>` is literal text for the reader to replace, and G is the grant text of section 8.3, or `''` when that is empty | |
| `warnings` | array of strings | sentences for a human reader. Their wording is not part of the format and a consumer MUST NOT parse it. | |
| `ffi_modules` | array of strings | sorted names, each the text up to its first `.`, of every module given as literal text in the module argument of `py`, `py_int`, `py_float`, `py_json` or `py_new`, anywhere in the program as loaded - the audited file and every file it imports | 2.60 |
| `loops_unshown` | integer | loops in the audited file whose termination the reference's rule (velaris-lang SPEC.md section 9.5) does not show, including loops inside inline function values | 2.62 |
| `contract_coverage` | array of strings | functions in the audited file that take or return a `List`, a `Map` or a record and have no `requires` or `ensures` | 2.62 |
| `fs_paths` | object | `read` and `write`: sorted arrays of path text, exactly as written, not resolved. `read` holds the literal first argument of every `read_file` and `file_exists` call anywhere in the program as loaded; `write`, of every `write_file` call. `read_any` and `write_any`: true when some such call's argument is not a literal. | 3.0 |
| `net_hosts` | object | `hosts`: a sorted array. For each literal URL given as the first argument of `fetch`, `post` or `fetch_status`, or the second of `request`, anywhere in the program as loaded: `https://` is put in front if it begins with neither `http://` nor `https://`; the host is lower-cased and trailing dots removed; the entry is the host, or `host:port` when the URL writes a port. From velaris-lang 3.3.0 an IPv6 host is written in brackets (`[::1]`, `[::1]:443`), so `host:port` is never ambiguous, and any of `, @ [ ] %` in a host is percent-encoded (a `net:` grant, section 5.2). `any`: true when some such argument is not a literal, or has no host. | 3.0 (IPv6 bracketed, 3.3) |

Two scopes are at work, and they differ. `effects`, `functions`,
`loops_unshown` and `contract_coverage` describe the functions defined
in the audited file. `ffi_modules`, `fs_paths` and `net_hosts` read the
literals of every function loaded, including functions in imported
files that the program never calls, so they can list more than the
program's own calls reach.

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
- any other name: the name itself (always one of the seven, since a
  `uses` clause naming anything else no longer compiles, section 3.2).

The results are joined with commas. Because the paths and hosts are
escaped, `safe_command` always parses, and `parse_budget` of it
reproduces the grants it was built from.

### 8.4 What an audit does not tell you

- **It reads literals only.** A path or URL built at runtime is
  reported through `read_any`, `write_any` and `any`. For modules there
  is no such flag in version 1: a module named by a computed value is
  absent from `ffi_modules`, and nothing says one exists. A program
  whose `ffi_modules` is `["math"]` may also call a module whose name
  it builds while running. Under the `safe_command`'s `ffi:math` that
  call is refused (E311), so the gap errs toward refusal at runtime,
  but a reader of the audit is not told of it. Open question Q4.
- **`safe_command` is the narrowest budget the audit can write, not a
  budget known to be enough, and not one known to be safe.** It grants
  every declared effect, `ffi` included, and a relative path in it
  resolves against the working directory of whoever runs the command.
- *Resolved in 0.2 (velaris-lang 3.3.0).* Version 0.1 recorded that in
  velaris-lang 3.1.1 `safe_command` was wrong in three cases: an IPv6
  literal host written without brackets (`net:::1`) parsed as a
  different host; a path literal containing `,` or `@` produced text
  that did not parse, or parsed as something else; and an unknown name
  in a declaration was copied into it. From 3.3.0 IPv6 hosts are
  bracketed and `, @ [ ] %` are percent-encoded in paths and hosts
  (sections 5.1, 5.2), so `safe_command` round-trips; and an unknown
  name in a `uses` clause no longer compiles (section 3.2), so none
  reaches the audit. This closes open question Q5.
- **When `ok` is false, no field bounds anything.**

## 9. velaris.capabilities/0 (provisional)

**This section is provisional.** The reference implementation does not
read or write this document yet. It is defined now so that tools can be
written against a fixed text, and so that the reference has a text to
implement. Until the reference ships it, this section may change
without the schema name changing; the `/0` says so. The form the
reference ships will be `velaris.capabilities/1`.

### 9.1 What it is for

A baseline is a file committed to a repository. For each program it
records the grants the program's audit says it needs. A check in CI
compares each program's current audit with its entry, and fails when
the program has come to need something the entry does not cover: a new
effect, a new module, a path, a host. A tool may narrow an entry when a
program comes to need less - the ratchet moves one way on its own - but
an entry is widened only by someone editing the file, where the change
shows in review.

A baseline records what a program's text names, not what a run may do.
It is not a budget, though its grants are written in the budget
grammar, and an entry's grants joined with commas make a budget an
operator may choose to run under.

### 9.2 The document

A JSON object with these fields, and no others:

| Field | Required | Meaning |
|---|---|---|
| `schema` | yes | `"velaris.capabilities/0"` |
| `generated_by` | no | informative: what wrote the document |
| `programs` | yes | an array of entries, sorted by `file`, no two with the same `file` |

Each entry has these fields, and no others:

| Field | Required | Meaning |
|---|---|---|
| `file` | yes | the program's entry file, relative to the directory holding the baseline; `/`-separated; not beginning with `/`; no empty, `.` or `..` component; no `\` |
| `grants` | yes | an array of grants, possibly empty |
| `note` | no | text for people; tools MUST NOT read meaning into it |

Grants in a baseline use the grammar of section 4 with these
restrictions, so that an entry means the same thing on every machine:

1. **No counts.** A count is an operator's decision about a run, not a
   property of a program's text.
2. **One module per grant**: `ffi:math` and `ffi:json`, never the
   continuation form.
3. **Paths as the program writes them**, compared as text (section 9.4)
   and never resolved against a file system. No `,` or `@` in a path.
4. **Hosts lower case**; IPv6 addresses in brackets.
5. **Reduced**: sorted by code point, no repeats, and no grant that
   another grant in the same entry covers (section 9.4). So an entry
   never holds `ffi` together with `ffi:M`: `ffi` covers `ffi:M`
   (section 9.4), and as a budget `ffi` grants every module anyway
   (section 4.3), so the `ffi:M` would add nothing.

The schema,
[schemas/velaris.capabilities.0.schema.json](schemas/velaris.capabilities.0.schema.json),
checks the shape of all of this; it cannot check sorting, reduction or
the port range, and `tools/validate.py` checks the sorting.

### 9.3 From an audit to grants

A program's current grants are derived from a `velaris.audit/1`
document D of it:

1. If D's `ok` is false, the program has no current grants and the
   comparison fails: a program that does not compile cannot be
   compared.
2. If a name in D's `effects` is not one of the seven effects, the
   derivation fails.
3. For each name e in D's `effects`:
   - `io`, `env`, `clock`, `rand`: e.
   - `ffi`: one `ffi:M` for each M in `ffi_modules`; `ffi` if it is
     empty.
   - `fs`: for each direction d, `read` and then `write`: `fs:d` when
     `fs_paths.d_any` is true, or when any path listed for d contains
     `,` or `@`; otherwise one `fs:d:P` for each path P listed for d.
     If this produced nothing, `fs`.
   - `net`: `net` when `net_hosts.any` is true, when `hosts` is empty,
     or when any entry of `hosts` contains more than one `:` or any of
     `,`, `@`, `/`, `*`. Otherwise one `net:E` for each entry E.
4. Reduce (section 9.2, rule 5).

These are the rules of section 8.3 with the reference's `safe_command`
defects closed in the conservative direction. An entry with more than
one `:` is an IPv6 address with or without a port, and
`velaris.audit/1` cannot say which; where the audit's text is
ambiguous, the derivation takes the unscoped grant, which a scoped
baseline entry does not cover, so the ambiguity surfaces as a failure
someone has to look at.

### 9.4 When one grant covers another

A grant b covers a grant c when one of these holds:

- b and c are the same text, after the path normalisation N below;
- b is `ffi` and c is `ffi:M`;
- b is `fs` and c is any `fs` grant;
- b is `fs:d` and c is `fs:d:P`;
- b is `fs:d:Q` and c is `fs:d:P`, and N(P) = N(Q), or N(P) begins
  with N(Q) followed by `/`, or N(Q) is `.` and N(P) is relative and is
  neither `..` nor begins with `../`;
- b is `net` and c is any `net` grant;
- b is `net:H` or `net:H:p`, c is `net:h` or `net:h:q`, the port p is
  absent from b or equal to q (so a grant with a port does not cover
  one without), and either H and h are both wildcards and equal, or h
  is not a wildcard and H matches it (section 5.2).

N(P) is P with every run of `/` made one `/`; every `.` component
removed; every `..` removed together with the component before it,
when there is one and it is not `..`; a `..` directly after a leading
`/` removed; a trailing `/` removed; and an empty result made `.`. So
N(`./data/`) is `data`, N(`a/../b`) is `b`, and N(`../x`) is `../x`.
`\` is not a separator (open question Q7), and comparison is
case-sensitive.

This is the relation of section 5.5, applied grant by grant, with paths
compared as text instead of resolved.

### 9.5 The ratchet

For each program a tool checks - which files it checks is the tool's
choice, usually every `.vel` file in the repository:

- **R1.** If the baseline has no entry for the program, the check fails
  and reports the program's current grants.
- **R2.** If the current grants cannot be derived (section 9.3, steps 1
  and 2), the check fails.
- **R3.** Otherwise the check passes when every current grant is
  covered by some grant of the entry, and fails when one is not, naming
  each grant that is not covered.
- **R4.** When the check passes, a tool MAY replace the entry with the
  program's current grants - that is the ratchet tightening. A tool
  MUST NOT write an entry the existing entry does not cover unless a
  person asks for it in so many words (for example with a flag named
  for accepting a widening), so that every widening arrives as a change
  to the baseline in review.
- **R5.** An entry for a file that no longer exists is not a failure,
  and a tool MAY remove it.

### 9.6 Example

[examples/velaris-lang.capabilities.json](examples/velaris-lang.capabilities.json)
is what a baseline at the root of velaris-lang would hold for four of
its example programs, derived under section 9.3 from the four audits in
[examples/audits/](examples/audits):

```json
{
  "schema": "velaris.capabilities/0",
  "programs": [
    {"file": "examples/effects.vel",
     "grants": ["clock", "fs:read:report.txt", "fs:write:report.txt", "io", "rand"]},
    {"file": "examples/pipeline.vel", "grants": ["io"]},
    {"file": "examples/stress.vel",
     "grants": ["clock", "env", "ffi:datetime", "ffi:math", "ffi:sqlite3", "io",
                "net:raw.githubusercontent.com"]},
    {"file": "examples/wordcount.vel", "grants": ["fs:read", "io"]}
  ]
}
```

If `examples/pipeline.vel` came to read a file whose name it is
given on its command line, its audit would add `fs` with `read_any`,
its current grants would become `["fs:read", "io"]`, and the check
would fail on `fs:read` until someone widened the entry.

## 10. Conformance

Conformance is defined by the suite in the reference implementation's
repository, not by this text. From velaris-lang 3.2.0, its
ARCHITECTURE.md names that suite: `check_termination.py`,
`check_sandbox.py`, `check_refusals.py`, `check_fallible.py` and
`check_library.py`. An implementation claiming velaris.capabilities
compliance must pass the subset of those five that does not require
the prover - that is, each suite as it runs when the Z3 prover is not
installed. Each suite detects the prover and, without it, skips the
checks that need it or asserts the runtime fallback instead.

The claim covers sections 3 to 8: the effects and the transitive rule,
the grant grammar, scoped grants and counts, enforcement, and
`velaris.audit/1`. It does not cover `velaris.capabilities/0`, which no
suite exercises, because the reference does not read it yet.

| Suite | What it holds | Sections |
|---|---|---|
| `check_sandbox.py` | escape attempts against a budget given on the command line: each effect refused; an effect hidden two helpers down; a refusal caught and carried on; the module list through `py`, `py_json`, `py_new` and a submodule path; the attribute-chain bound of section 5.3 - codecs through json, os.system through os, importlib to another module, a builtins type through a value, a `__globals__`/`__class__` traversal, a foreign object through a handle - with a deep attribute inside the granted module and a two-module grant still running; additive `fs`, `net` and `ffi`; a path outside a prefix, a write under a read grant, `..`, and a symbolic link (POSIX only); a host outside the list, including a name when an address was granted; a port; a wildcard's parent domain; redirects to a granted and to an ungranted host; counts on `fs` and `net`; `env` under `io` | 4, 5, 6 |
| `check_library.py` | the same through the reference's library, its HTTP door's ceiling (section 5.5) and its MCP server; that the library and the server report the same audit; that `safe_command` round-trips for awkward paths and hosts (section 8.3); that every malformed budget raises a readable budget error and never a traceback (section 4.2); that the command line's `audit --json` is `velaris.audit/1` and validates against the schema (section 8) | 4, 5, 6, 8 |
| `check_refusals.py` | wrong programs refused with the right code, among them an undeclared effect (E300) | 3.2 |
| `check_fallible.py` | every fallible builtin refused when its failure is ignored, and its failure catchable - the redirect failure of G4 among them | 6, 8 |
| `check_termination.py` | the termination verdict for each of 44 adversarial loops, which `velaris.audit/1` reports as `loops_unshown` | 8 |

What the suite cannot yet do as a conformance suite:

- **It is written against the reference's interfaces.** It runs
  `python velaris.py` and imports the `velaris` module. An
  implementation in another language must be driven through an adapter
  that offers the same command line and library calls. No
  language-neutral harness exists in this version (open question Q8).
- **It does not test every rule stated here.** A reading of
  `check_sandbox.py` and `check_library.py` at 3.1.1 found no case for
  the points listed in open question Q9. From velaris-lang 3.3.0 several
  of them have cases - the attribute chain through a granted module,
  `ffi` together with `ffi:M`, IPv6 grants bracketed and not - added
  with the fixes; the rest remain untested. Passing the suite is
  evidence about the cases it holds, and no more.

## 11. Open questions

Each question is a point where this document records the reference's
behaviour, or where the reference's own text and behaviour disagree,
without settling what is right. Q1, Q2, Q3, Q5 and Q6 were open in
version 0.1 and are **resolved in 0.2** (velaris-lang 3.3.0); they are
kept here, marked resolved, so the record of what changed stays with the
question.

- **Q1. Unknown names in declarations. Resolved in 0.2.** Version 0.1
  asked whether a checker should reject a `uses` name that is not one of
  the seven. From velaris-lang 3.3.0 it does, with E300 naming the
  seven, so `velaris.audit/1`'s `effects` is always a subset of them
  (section 3.2).
- **Q2. "Grants are additive" and `ffi`. Resolved in 0.2.** Version 0.1
  followed the parser, which restricted `ffi` to the named modules when
  both `ffi` and `ffi:M` appeared, against the reference text's "Grants
  are additive". From velaris-lang 3.3.0 `ffi` is additive like `fs` and
  `net` - the wider grant wins - so text and parser agree (section 4.3).
- **Q3. The command line's audit. Resolved in 0.2.** Version 0.1
  recorded that `velaris audit FILE --json` printed a shape that is not
  `velaris.audit/1`. From velaris-lang 3.3.0 it prints
  `audit().as_dict()`, the same document as every other door (section 8).
- **Q4. No flag for a computed module name.** `velaris.audit/1` has
  `read_any`, `write_any` and `any`, and nothing for `ffi` (section
  8.4). A field such as `ffi_any` would be an addition within version 1.
  (Still open.)
- **Q5. `safe_command` for IPv6 hosts and awkward paths. Resolved in
  0.2.** Version 0.1 recorded the unbracketed IPv6 form and the paths
  that did not round-trip. From velaris-lang 3.3.0 IPv6 hosts are
  bracketed in the grammar, in `net_hosts` and in `safe_command`, and
  `, @ [ ] %` are percent-encoded in paths and hosts (sections 5.1, 5.2,
  8.3), so `safe_command` round-trips. Changing `net_hosts` to bracket
  IPv6 is a change to what that field contains; it is made here in a new
  format version, not within version 1 silently.
- **Q6. Stray forms the parser accepts. Resolved in 0.2.** Version 0.1
  recorded a count with non-ASCII digits, `ffi:M@N`, and `ffi:` with no
  module. From velaris-lang 3.3.0 each is a budget error (sections 4.2,
  5.3), and no malformed budget produces a traceback.
- **Q7. Windows paths in baselines.** Section 9.4 compares paths as
  text with `/` as the only separator, and case-sensitively. A program
  written for Windows may name `data\in.csv`; two spellings of one path
  then compare as different, and the check fails rather than passes -
  the safe direction, but noisy.
- **Q8. A conformance harness for other languages.** The suite drives
  the reference's command line and Python library (section 10). What
  would an implementation in another language run?
- **Q9. Rules stated here and not yet tested by the suite.** Partly
  addressed in 0.2. From velaris-lang 3.3.0 the suite covers a function
  argument that is a dotted path through a granted module's attributes
  (section 5.3), `ffi` together with `ffi:M` (section 4.3), and IPv6
  grants bracketed and not (section 5.2). Still untested: a URL without
  a scheme taken as HTTPS (section 5.2); an existence check under a
  write-only grant (section 5.1); `@0`, and a count spent by an
  operation that then fails (section 5.4).
- **Q10. The reference text's table.** Its row `...@N` reads as if a
  count could follow any grant; the reference accepts counts only on
  `fs` and `net` (section 4.2).
- **Q11. Attestation.** `velaris.audit/1` is unsigned and names no
  artifact digest. Carrying it as an in-toto predicate, with a
  predicate type of its own, would let a signed statement say which
  source file was audited (see PRIOR_ART.md). This version defines no
  predicate type.

## Appendix A. The reference binding

Informative: which builtins of velaris-lang 3.3.0 perform which
operations.

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
written in Velaris, and carry the effects of the builtins they call
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

## Appendix C. Changes

- **0.2**, 2026-09-11: tracks velaris-lang 3.3.0, which fixed the five
  defects the 0.1 extraction found. Resolves Q1 (an unknown name in a
  `uses` clause is rejected, section 3.2), Q2 (`ffi` grants are additive;
  the wider grant wins, section 4.3), Q3 (the command line's
  `audit --json` emits `velaris.audit/1`, section 8), Q5 (`safe_command`
  and `net_hosts` bracket IPv6, and the escaping rule holds `,`, `@` and
  the rest in paths and hosts, sections 5.1, 5.2, 8.3, 8.4), and Q6
  (a non-ASCII count digit, `ffi:M@N` and `ffi:` with no module are
  budget errors, sections 4.2, 5.3). Adds the percent-encoding escaping
  rule to sections 5.1 and 5.2. Notes in Q9 the rules the suite now
  covers. Section 2 still quotes velaris-lang SPEC.md sections 6, 7 and
  7.1 word for word - those sections did not change - so
  `tools/check_sync.py` still passes.
- **0.1**, 2026-09-11: first version, extracted from velaris-lang
  3.1.1.
