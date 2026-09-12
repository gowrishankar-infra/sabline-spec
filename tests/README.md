# The conformance corpus

Cases an implementation of the Velaris capability format runs to show
it conforms: one JSON file per case, each with what goes in and what
must come out. No case needs velaris-lang or Python. An implementation
reads the files, runs each case its own way, and reports pass or fail
for each. [CONFORMANCE.md](../CONFORMANCE.md) says which cases make up
which level and what a claim of conformance says; this file is the
runner contract - how each kind of case is run and compared.

The corpus is generated. velaris-lang's `build_conformance.py` writes
it from the tables of three of that repository's suites -
`check_sandbox.py`, `check_library.py` and `check_ratchet.py` - where
each entry is also asserted against velaris-lang. Each case's `from`
names its entry. Do not edit a case by hand: change the suite, and
regenerate. A drift test in both repositories' CI regenerates the
corpus and fails when the result differs from what is committed here.

## Layout

| Path | What it is |
|---|---|
| `index.json` | every case's id, level, kind and file; counts per level; the scenarios left out, and why |
| `case.schema.json` | JSON Schema (draft 2020-12) of a case file |
| `L1/`, `L2/`, `L3/` | the cases, one file each, named by id |
| `../schemas/` | the schemas an `audit` or `derive` case's output must validate against |

## A case

| Field | Meaning |
|---|---|
| `id` | unique; `L1-`, `L2-` or `L3-` and lower-case words |
| `level` | 1, 2 or 3 ([CONFORMANCE.md](../CONFORMANCE.md)) |
| `kind` | what to do with it: one of the ten kinds below |
| `description` | what the case shows, in a sentence |
| `spec` | the sections of [SPEC.md](../SPEC.md) it holds an implementation to |
| `from` | the suite table entry it was written from |
| `requires` | what the platform must provide for the case to run: `symlink` (a symbolic link can be made) or `stdlib` (the reference's standard library can be imported by name) |
| `known_limit` | null, or the known limit the case records ([Known limits](#known-limits)) |
| `input` | what goes in; its shape depends on `kind` |
| `expect` | what must come out; its shape depends on `kind` |

## Running cases

- Run each case on its own, in a fresh, empty directory, with nothing
  from another case. Where a case writes files, write them with `\n`
  line endings, UTF-8, and `/` in names read as a directory separator.
- Report every case: `pass`, `fail`, or `skip` with the reason. A case
  whose kind or field the runner does not understand fails - it never
  passes by default. A case may be skipped only when the platform
  cannot meet something in its `requires`, or when a tool the runner
  needs is missing (a JSON Schema validator); the report says which.
- Paths in expectations are compared after resolution only where this
  file says so. Everything else is compared exactly, as JSON values:
  objects as maps, arrays in order, unless this file says a list is
  compared as a set.

## The ten kinds

### `budget` (level 1)

`input`: `allow`, budget text, and/or `deny`, a comma-separated list of
effect names. `expect`: `{"valid": false}` or `{"valid": true, "grants":
G}`.

Parse `allow` as a budget (SPEC.md sections 4 and 5). If `deny` is
given, apply it as a denial (4.4) to the budget from `allow`. `allow`
present and empty is the empty budget.

A case that gives `deny` always gives `allow` too. What a denial alone
narrows is the runtime's default budget, which SPEC.md 4.6 leaves to
the runtime, so no case makes an implementation's default part of the
test. (Until velaris-spec 0.6.0 one case did, applying a denial to all
seven effects; the reference's default changed in velaris-lang 5.0 and
the case was rewritten to write its grants down.)

- `valid: false`: the implementation must refuse the budget as a whole.
- `valid: true`: the budget parses, and means `G`:

| Field of `G` | Compared as |
|---|---|
| `effects` | the set of granted effects |
| `ffi` | present when `ffi` is granted: `"any"`, or the set of module names |
| `fs` | present when `fs` is granted: `"any"` (every path, both directions), or the set of `{direction, path}` grants; `path` null is any path in that direction. A path is the grant's text after percent-decoding, before resolution: resolve it with SPEC.md 5.1's R in the runner's working directory, resolve your parser's path the same way, and compare the results |
| `net` | present when `net` is granted: `"any"`, or the set of `{host, port}` grants, host lower-case and decoded, port null for any |
| `counts` | a map from `fs` and `net` to the run's count, holding only the effects that have one |

### `audit` (level 1)

`input`: `files`, a map of file names to Velaris source, and `entry`,
the file to audit. Write the files into an empty directory and produce
the file's `velaris.audit/1` document (SPEC.md 8). Every document, in
every audit case, must:

1. validate against `../schemas/velaris.audit.1.schema.json`;
2. have an `effects` that is sorted, has no repeats, and holds only the
   seven effect names;
3. have a `safe_command` whose grant text - everything after
   `--allow ` - parses as a budget (`''` is the empty budget).

Then, when `expect.ok` is false: the document's `ok` is false, and each
code in `expect.problems_include` is the `code` of one of its
`problems`. Nothing else is compared, since when `ok` is false no field
bounds anything.

When `expect.ok` is true: `ok` is true, and `effects`, `ffi_modules`,
`ffi_any`, `fs_paths`, `net_hosts` and `safe_command` equal the
expectation exactly; and `functions`, reduced to each entry's `name`,
`effects` and `can_fail`, in order, equals `expect.functions`. The
fields that depend on a prover - `status`, `proven_share` - and the
wording of `warnings` are never compared.

### `run` (level 2)

`input`: `fixture` (always `"sandbox"`), `source`, `allow` and, where
the case denies, `deny` as well, both as for `budget`, and `args`, the
program's arguments. `expect`: an `outcome` and what the run must and
must not leave behind. Every `run` case names its budget: as with
`budget` cases, no case leaves the implementation's default (SPEC.md
4.6) to do the work.

Set up the fixture, put the values of the placeholders into `source`,
`allow`, `deny`, `args` and every string of `expect`, and run the
program under the budget with those arguments, from `{ROOT}`.

The sandbox fixture:

| Placeholder | Value |
|---|---|
| `{ROOT}` | a new, empty directory; the run's working directory |
| `{DATA}` | `{ROOT}/box/data`, holding `a.txt` with the text `inside` and a line break |
| `{OUT}` | `{ROOT}/box/out`, an empty directory |
| `{OUTSIDE}` | `{ROOT}/outside.txt`, holding `outside` and a line break |
| `{PORT_A}` | the port of an HTTP/1.1 server on `127.0.0.1`: a GET of `/go` answers 302 with `Location: http://localhost:{PORT_B}/landed`; a GET of any other path answers 200 with the body `hello` |
| `{PORT_B}` | the port of a second server on `127.0.0.1`, answering the same way |

Paths are written with `/` on every platform. The name `localhost` must
reach the servers. When the case `requires` `symlink`, also make
`{DATA}/link.txt` a symbolic link to `{OUTSIDE}`; if the system will not
make one, skip the case and say so.

| `outcome` | The run passes when |
|---|---|
| `refused` | the run ended in a refusal (SPEC.md 6, G3) with the code `code` - not a normal end, and not a failure the program handled; no string of `stdout_excludes` appears on its standard output; no path of `must_not_exist` exists afterwards; and each string of `stdout_includes` appears on its standard output |
| `completed` | the run ended normally - in a command line, exit status 0 - and each string of `stdout_includes` appears on its standard output |

`stdout_excludes` holds the words the programs print only if they got
past the refusal. A refused case whose `stdout_includes` is not empty
shows that the program did run up to the refused operation.

### `derive` (level 3)

`input`: `tree`, a map of file names to Velaris source, and `root`, the
directory of the tree to record (`.` for the whole tree). Write the
tree, and write the baseline for `root` with the implementation's own
writer (SPEC.md 9.2 to 9.4). The document must validate against
`../schemas/velaris.capabilities.1.schema.json`, and its `surface` and
`programs` must equal `expect` exactly; `velaris_version` and `date`
are the writer's own and are not compared.

### `check` (level 3)

`input`: `tree`, `root`, `baseline` and `change`. `expect`: a verdict.

1. Write the tree.
2. Put the baseline at `<root>/velaris.capabilities`:
   - `{"from_tree": true, "edit": E}`: write it with the
     implementation's own writer from the tree as it is, then apply `E`
     when it is not null (below);
   - `{"absent": true}`: there is none;
   - `{"text": T}`: write `T`, as it is.
3. Apply `change`: each file's new text, or `null` to delete it. Names
   are relative to the tree's top, like the tree's.
4. Check `root` against its baseline (SPEC.md 9.6) and compare the
   verdict.

An edit is what a person does to the file: `velaris_version`, when
given, replaces the document's; each key given under `surface` replaces
that key of the surface; for each program named under `programs`, each
key given replaces that key of the program's entry.

A verdict:

| `verdict` | Meaning |
|---|---|
| `pass` | the check compared, found no widening, and passed |
| `widened` | the check compared and failed; `widenings` lists every widening |
| `cannot-compare` | the check could not compare - no baseline, or one it cannot read - and did not pass (SPEC.md 9.6) |

For `pass` and `widened`, the implementation's widenings, written as
below, must be exactly `widenings`, compared as a set:

| Widening | Fields |
|---|---|
| a grant | `kind: "grant"`, `grant`, `rules` - the rules it fails among W1 and W3 - and `programs`, sorted: every program that needs it, when it is outside the surface (each fails W1), and otherwise each recorded program whose own entry does not cover it (W3) |
| a count | `kind: "count"`, `effect` (`fs` or `net`), `program`, `current` - the program's count, null for no bound - and `rules`, among W2 and W4; one per program |
| a function | `kind: "function"`, `program`, `function`, `gained` - the effects it declares now and did not in the baseline, sorted - and `rules: ["W5"]` |

Rules are listed in order, W1 first. Narrowing, notes and warnings are
not compared: SPEC.md 9.6 says a check SHOULD report them, not MUST.

### `sequence` (level 3)

`input`: `tree`, `root`, and `steps`. `expect.steps`: one verdict per
step. Write the tree and its baseline, written from it, once. Then for
each step, in order, on the tree as the previous steps left it: apply
the step's `change`; apply its `edit`, when not null, to the baseline
file; when `rewrite` is true, write the baseline again from the tree,
as a person asking for it; when `delete_baseline` is true, delete the
baseline; then check, and compare with the step's verdict. The check at
every step is against the baseline as the file stands - never against
the tree of the step before.

### `write-guard` (level 3)

`input`: `tree`, `root`, `change`. Write the tree and its baseline;
apply `change`; then ask the implementation's writer to write the
baseline again the way a person would without saying in so many words
to replace it. The case passes when the writer refuses and the file is
byte for byte what it was (SPEC.md 9.6, last paragraph).

### `covers` (level 3)

`input`: `grant` and `other`, two baseline grants (SPEC.md 9.2).
`expect.covers`: whether `grant` covers `other` under SPEC.md 9.5.

### `reduce` (level 3)

`input.grants`: a list of baseline grants. `expect.grants`: the list
reduced under SPEC.md 9.2 rule 5 - sorted by code point, without
repeats, without a grant another covers, and of two that cover each
other the first in code-point order - compared exactly, in order.

### `bound` (level 3)

`input`: `source` and `function`. Load the source as one file and
compute, for the function, the bound B of SPEC.md 9.4 on `fs` and on
`net` operations. `expect`: `{"fs": n, "net": n}`, each a whole number
or null for no bound.

## Requirements

- `symlink`: the case needs a symbolic link in its fixture.
- `stdlib`: the case's program imports the reference's standard
  library by name (`import "std.vel"`, `import "http.vel" as http`).
  The library is Velaris source, in velaris-lang's `stdlib/`; an
  implementation that provides it runs the case, and one that does not
  skips it.

## Known limits

Five `check` cases carry a `known_limit`: the ratchet's limits, listed
in velaris-lang's CHANGELOG (4.0, "What the ratchet cannot do") and in
SPEC.md 9.8. Each records what the reference does today - two changes
that widen and pass, three that do not widen and fail - and the case
expects that outcome, so that another implementation matches it rather
than guessing, and so that a change to it is a change to the corpus,
in review. A known-limit case is required like any other.

## The report

A runner reports one result per case. The reference writes its report
with `velaris conformance --json`; another runner may write the same
shape:

```json
{
  "schema": "velaris.conformance/1",
  "implementation": {"name": "velaris-lang", "version": "4.2.1"},
  "corpus": "where the corpus was read from",
  "levels_run": [1, 2, 3],
  "levels": {"1": {"name": "Declaration", "cases": 298, "passed": 298,
                   "failed": 0, "skipped": 0, "unshown": 0}},
  "conformant": [1, 2, 3],
  "results": [{"id": "L2-fs-read-outside-prefix", "level": 2,
               "kind": "run", "result": "pass", "detail": "",
               "known_limit": false}],
  "verdict": "one line"
}
```

`unshown` counts skips for a missing tool rather than a case's own
requirement; a level with one is not shown conformant.

## What the corpus leaves out

`index.json`'s `excluded` lists every scenario of the three suites'
tables that is not a case, with the reason. Thirteen, all from
`check_sandbox.py`:

- six attempts to reach an ungranted Python module through a granted
  one - `codecs` through `json`, `os.system` through `os`, `importlib`,
  a `builtins` type through a value, a `__globals__` traversal, a
  foreign object through a handle. SPEC.md 5.3 binds every
  implementation to refuse them, but each case depends on Python's
  object model;
- four honest programs that call a granted Python module, which need a
  Python host to run;
- a run given no budget, which SPEC.md 4.6 leaves to the implementation;
- two about the reference command line's own flags.

Not scenarios, and so not listed there: what `check_ratchet.py` asserts
about the reference's own interfaces beyond the verdict - the call
chain and line a finding names, `velaris review` and its risk word, the
SARIF log, the text of warnings and notes, `velaris fmt` - and what
`check_library.py` asserts about the reference's library, doors and MCP
server.

## The language the cases use

The programs are Velaris (velaris-lang SPEC.md); a runner needs enough
of the language to check and run them. Level 2's programs use
functions with `uses` clauses and `or fail`, `requires` and `ensures`
(in one case), `let` with and without a type, assignment, `if`,
`while`, `for ... in ... to`, `check`/`ok`/`fail`, `try`, `import
"std.vel"` (one case, for `sort`), and the builtins `print`, `format`,
`length`, `now`, `random`, `env`, `read_file`, `write_file`,
`file_exists`, `fetch`, `fetch_status`, `py`, `py_json` and `py_new`.
Every level 2 case that calls into the host names a module, or an
effect, its budget does not grant, so it is refused before any host
code runs. Levels 1 and 3 add `args`, `to_text`, `lower`, `post`,
`request` and `py_int`, a comment, a named import (`import "http.vel"
as http`), and imports of relative files, including one from outside
the checked directory (`import "../ext/app.vel"`).
