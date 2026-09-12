# Submitting Velaris to agentlanguages.dev

A draft for the author. **Nothing has been sent.** No fork, no branch,
no pull request, no email. What follows is what the catalogue asks for,
read from its own repository on 2026-09-12, and a filled-in entry to
review before sending.

The catalogue: *Agent Languages*, edited by Alasdair Allan,
<https://agentlanguages.dev>, mirrored at
<https://research.tedneward.com/places/agentlanguages.html>. Source:
<https://github.com/aallan/agentlanguages>. It tracked 41 projects at
reading. Velaris is not among them.

## 1. What it asks for

It is a pull request, not a form and not an email. From CONTRIBUTING.md:

1. Fork <https://github.com/aallan/agentlanguages>.
2. Add **one** Markdown file at `src/content/languages/<slug>.md`. The
   filename is the URL slug: lowercase, hyphen-separated, no spaces.
   For Velaris that is `src/content/languages/velaris.md`.
3. Write a body. "A non-empty body renders a detail page at
   `/languages/<slug>/`, and in practice every entry in the catalogue
   has one" - treat it as expected, not optional. 200 or more words
   showing first-hand familiarity.
4. Open the pull request using the new-language template.

**Inclusion criteria.** A project qualifies if it is "designed for
LLMs/agents to author code". The signals it lists that Velaris meets:
mechanically checkable contracts (requires/ensures, SMT verification);
agent-coordination primitives (it names "capability-gated effects" and
"hash-chained evidence bundles" explicitly); and agent-facing tooling
shipped with the compiler (structured-JSON diagnostics, MCP servers).
A tool that merely *uses* an LLM at run time is out of scope; Velaris
is a language, so this is not a problem.

**Camp.** Self-classify, and justify in the PR thread. The maintainer
makes the final call, and "several entries have been merged with a
different secondary camp from the one submitted".

**What it never asks for.** Star, fork and commit counts - a scheduled
action fetches those weekly into `src/data/stars.json`. Do not put them
in the entry.

**Tone.** "Descriptive, not promotional. The catalogue is a reference,
not advocacy." One-liners read as observation, not pitch. It says the
word "elegant" is almost always wrong and that "explicit", "verified"
and "deterministic" are usually right. British English, house style.

**Review.** Checked for fit, accuracy and tone. "Accuracy review means
the claims in a submission get checked against the source, not taken on
trust" - and it cuts both ways: past reviews have corrected a figure a
submitter overstated and one a submitter understated to their own
disadvantage. Expect an editorial pass; the substance stays the
submitter's, and every edit is explained in the thread.

**Licence.** Entries are CC BY 4.0; code is MIT. Opening a pull request
agrees to publication under those terms, and the author keeps copyright.
Note that velaris-spec is CC0 and velaris-lang is MIT, so there is no
conflict in submitting a description of them under CC BY 4.0.

## 2. Frontmatter, filled in

Every value below is checkable against the two repositories. `crossrefs`
is the field the guide says is worth bothering with: "two to four
comparisons that say what this language shares with a neighbour and
where the two part company", written contrastively. The four chosen are
the four nearest projects found in the prior-art read (PRIOR_ART.md,
"The AI-first language field"). Each `slug` matches an existing file.

```yaml
---
name: Velaris
camp: verification
spans_camps: [orchestration]
one_liner: "Effects declared in signatures, a budget the operator writes and the runtime refuses against, and a committed baseline for a repository's capability surface."
url: https://github.com/gowrishankar-infra/velaris-lang
repo: gowrishankar-infra/velaris-lang
paper: null
author: Palakurthi Gowri Shankar
implementation_language: Python
compilation_target: Interpreter, with an LLVM JIT for pure numeric and text code
license: MIT
maturity: working_compiler
date_appeared: 2026-08
agent_tooling: [LLM.md, MCP server, SARIF, structured-JSON diagnostics, VS Code extension]
key_idea: |
  A function's signature names which of seven effects it may perform, and
  the compiler checks the declaration across the whole call graph. What a
  run may actually reach is a separate document: a budget the operator
  writes, scoped to paths, hosts, modules and operation counts, which the
  runtime refuses against before each operation, in a way the program
  cannot catch. Contracts are discharged by Z3 where it can settle them
  and checked at run time where it cannot. A repository commits a
  baseline of the capability surface its programs need, and a CI check
  fails any change needing more.
crossrefs:
  - slug: boruna
    name: Boruna
    camp: orchestration
    relation: "Same diagnosis, and the closest neighbour here. Both declare effects on the function and gate them at run time against an operator's policy. Boruna records the run - hash-chained evidence bundles that replay to identical outputs - where Velaris records the source text, as a separately published format with an in-toto predicate and SARIF output. Boruna parses ensures without enforcing it and has no prover; Velaris discharges contracts with Z3. Boruna grants nothing by default, where Velaris without a budget grants all seven effects."
  - slug: thermite
    name: Thermite
    camp: verification
    relation: "Nearest on verification, and ahead of it: req/ens/fx on every function, obligations settled separately on a five-rung ladder across Verus, Z3 and Lean, against Velaris's single Z3 tier. The divide is who writes the policy. Thermite derives a seccomp filter from the program's own fx clauses; a Velaris budget is written by the operator, may be narrower than what the program declares, and is refused against at each operation."
  - slug: vera
    name: Vera
    camp: verification
    relation: "The same verification shape reached independently: mandatory requires/ensures/effects, Z3 where it decides and a compiled runtime guard where it does not, a conformance corpus and a written specification. Vera declares and checks effects but bounds no paths or hosts at run time and keeps no audit record; Velaris adds the operator's budget and a published document of the declared surface. Vera's literal-provenance rule for SQL has no counterpart in Velaris."
  - slug: ailang
    name: AILANG
    camp: verification
    relation: "Same arrangement, different granularity. Both put effects in the signature and have the operator grant them outside the program - AILANG at the command line with --caps, not wideable from within. AILANG grants whole categories; a Velaris grant is scoped to paths, hosts, modules and operation counts. AILANG has no contracts, no prover and no audit record."
history:
  - when: "August 2026"
    what: "First release, with effects, types, contracts and Z3 proofs."
  - when: "September 2026"
    what: "The capability format published separately under CC0 with a conformance corpus of 444 cases, and an in-toto predicate type for the audit."
benchmark:
  label: "Velaris, Deno and Python on 63 programs"
  url: https://github.com/gowrishankar-infra/velaris-lang/tree/main/benchmark
---
```

Two judgement calls to defend in the thread if asked. **Camp:** primary
`verification`, secondary `orchestration`. The prover and the contracts
are the larger half, but the budget and the audit are coordination
machinery, and the catalogue files Boruna the other way round on the
same pairing - the maintainer may prefer `orchestration` primary.
**`compilation_target`:** Velaris interprets and JITs part of what it
runs, which is not one of the tidy values other entries use; state it
plainly rather than claim a target it does not have.

## 3. The description, in the catalogue's house style

One paragraph, for the body of the entry or for the PR. Every figure in
it is checkable; none is rounded in Velaris's favour.

> Velaris is a small language for running code that nobody read. A
> function's signature declares which of seven effects it may perform -
> `io`, `env`, `fs`, `net`, `clock`, `rand`, `ffi` - and the compiler
> checks the declaration across the whole call graph, so an undeclared
> effect reached through three helpers is a compile error. What a run
> may actually touch is written separately, by the operator rather than
> the author: a budget scoped to paths, hosts, modules and operation
> counts, which the runtime refuses against before the operation
> happens and in a way the program cannot catch. Contracts are
> discharged by Z3 where it can settle them and compiled to runtime
> checks where it cannot, with a proof that exhausts its time budget
> saying so rather than falling silently back. A repository can commit
> a baseline of the capability surface its programs need, and a CI
> check fails any change that needs an effect, path, host, module or
> operation count the baseline does not grant, and goes on failing
> until a person edits the baseline. The capability format is not part
> of the implementation: it is published separately under CC0, with a
> conformance corpus of 444 cases that an implementation in any
> language can run, an in-toto predicate type for the audit it defines,
> and SARIF output for code scanning. On a benchmark of 63 programs -
> 56 with one defect, 7 correct - each written three times, Velaris
> caught 54 of the 56 defects, 42 of them before running, against 32
> for Deno and 28 for Python, with no false positive from any of the
> three; the numbers are the project's own.

Notes on the wording, against the catalogue's tone rule: no "elegant",
no "powerful", no "seamless"; "explicit", "verified" and "deterministic"
are the register it asks for. The benchmark sentence attributes the
numbers to the project, which the guide names as a typical editorial
correction - better to do it in the submission than to have it done.
The last clause of the contracts sentence is included because it is a
limitation as much as a feature.

## 4. Before sending

- Re-read the entry against the current release. It is written against
  velaris-lang 4.4.0 and velaris-spec 0.5.3; if either moves first,
  check the corpus count, the effect list and the benchmark figures.
- Check the four `crossrefs` slugs still resolve to files in
  `src/content/languages/` - `boruna.md`, `thermite.md`, `vera.md`,
  `ailang.md` all existed at reading.
- A body of 200+ words is expected. Section 3 is one paragraph; the
  guide's suggested headings are `## The thesis.`, `## What it looks
  like.`, `## Distinctive moves.`, `## Maturity.`, `## Agent tooling.`
  A code sample goes inline in the body as raw HTML, with token classes
  `kw`, `ty`, `ct`, `str`, `num`, `op`, `sl`, `cm`, and no blank line
  inside a `<pre>` followed by an indented line.
- One conflict of interest worth naming in the thread, since the
  catalogue's accuracy review cuts both ways: Vera is the maintainer's
  own language, and the crossref above says Velaris does something it
  does not. It is written to be checkable rather than flattering, and
  the thread is the place to say so plainly.
