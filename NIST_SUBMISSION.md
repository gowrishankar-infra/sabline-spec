# Input to NIST's AI Agent Standards Initiative: declared capability for code and tools that agents run

**Status: a draft, not sent.** Released under CC0 1.0, like the rest of
this repository.

## There is no open call to send this to

Checked on 2026-09-11. The AI Agent Standards Initiative, announced by
NIST's Center for AI Standards and Innovation (CAISI) on 2026-02-17
(<https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative>),
has taken input three times, and every window has closed:

| Call | Deadline | Status |
|---|---|---|
| CAISI, "Request for Information Regarding Security Considerations for Artificial Intelligence Agents", 91 FR 698, docket NIST-2025-0035 | 2026-03-09, 11:59 p.m. ET | closed; NIST summarised the responses as NIST AI 800-5 (2026-05-18) |
| NCCoE concept paper, "Accelerating the Adoption of Software and AI Agent Identity and Authorization" (AI-Identity@nist.gov) | 2026-04-02 | closed; "Reviewing Comments" |
| CAISI listening sessions on barriers to AI adoption | 2026-03-31 (extended from 2026-03-20) | closed |

The Initiative says NIST "will leverage a full toolbox for public
input, including convenings, RFIs, listening sessions, and other
approaches"; no date for the next is published. This document is
therefore written as a general submission, arranged so that it can be
sent to the next call. Channels that are open now, none of them a call
for agent standards:

- the mailbox of NIST's SP 800-53 control overlays for securing AI
  systems (COSAiS), overlays-securing-ai@list.nist.gov, whose concept
  paper includes single-agent and multi-agent use cases;
- the NCCoE identity and authorization project, whose concept paper
  says its next steps "could include development of a draft project
  description and a call for collaborators".

Federal Register calls take comments only through regulations.gov and
post them "without change or redaction". This document holds nothing
that should not be public.

## Respondent

Palakurthi Gowri Shankar, an individual, maintainer of sabline-lang
(<https://github.com/gowrishankar-infra/sabline-lang>) and sabline-spec
(<https://github.com/gowrishankar-infra/sabline-spec>). Contact: [to be
filled in before sending].

## What this bears on

The Initiative's first two pillars: "Facilitating industry-led
development of agent standards and U.S. leadership in international
standards bodies" and "Fostering community-led open source protocol
development and maintenance for agents". Of the questions in the closed
CAISI RFI, it answers parts of:

- 2(a)ii, "Agent system-level controls, such as ... data or tool
  restrictions";
- 2(e), "Which cybersecurity guidelines, frameworks, and best practices
  are most relevant to the security of AI agent systems?";
- 3(b), "how could the security of a particular AI agent system be
  assessed and what types of information could help with that
  assessment?";
- 4(a), "In what manner and by what technical means could the access to
  or extent of an AI agent system's deployment environment be
  constrained?".

It also bears on the NCCoE paper's question "How do we establish 'least
privilege' for an agent, especially when its required actions might not
be fully predictable when deployed?".

## Summary

An agent that writes code, or calls a tool, can do whatever that code
or tool can do. Sabline is a small programming language in which that
is stated where it can be checked: each function's signature declares
which of seven effects it may perform, the compiler checks the
declaration across the whole call graph, and the runtime refuses any
operation outside a budget the operator writes, before the operation
happens. A repository can commit a baseline of what its programs need,
and a check fails any change that needs more. The format - the effects,
the grant grammar, what a runtime must refuse, the audit document and
the baseline - is published separately under CC0 as sabline-spec, with
a conformance corpus of 444 cases any implementation can run, and
sabline-lang implements it. What this offers the Initiative is that
format, its corpus and its limits, as one worked example of a
declaration of agent capability that two implementations can be tested
to agree on.

## 1. The problem

Code written by a model is increasingly run by people who have not read
it, and tools are called by agents on behalf of people who did not
choose them one by one. Review is the step that gives: where code
arrives faster than people read it, the person deciding whether to run
it has no statement of what it may do that they can check without
reading it. Capability can also be assembled a little at a time. Hills,
Caspary and Cooper Stickland (arXiv:2607.02514) show that a coding
agent pursuing a covert task across pull requests can spread it so that
no single diff looks decisive, and that monitors reading one diff at a
time miss it. A comparison of each change with the one before sees each
step alone.

## 2. A declaration that is checked, and a budget that is enforced

- **Effects in signatures.** `fn save(path: Text, body: Text) uses fs`.
  There are seven effects: `io`, `env`, `fs`, `net`, `clock`, `rand` and
  `ffi` (calling the host language). The rule is transitive and checked
  before the program runs, so a declaration bounds what any call can do,
  at any depth, and can be read without the body.
- **A budget, at run time.** The operator writes grants in a small
  grammar: `io,fs:read:./data,net:api.example.com:443@100` narrows `fs`
  to a direction and a path, `net` to a host, port or one-label
  wildcard, `ffi` to named modules, and counts the operations of a run.
  Every operation is checked when it is attempted; a refused one does
  not happen and ends the run, and the program cannot catch the
  refusal. The budget is checked against what a run attempts, not what
  the program declares.
- **An audit before running.** `sabline.audit/1` is a JSON document of
  what a program declares and names - effects, paths, hosts, modules,
  bounds on file and network operations - and the narrowest budget to
  run it under.
- **Bound to the bytes it describes.** sabline-spec defines an in-toto
  predicate type that binds an audit to the digests of the source files
  audited. sabline-lang 4.2.0 and later write such Statements
  (`sabline attest`); its release workflow signs one for an example
  program with cosign and with sigstore-python and verifies both. A pull
  request listing the type in in-toto's predicate directory is
  prepared.

## 3. The ratchet: holding a repository to what it declared

`sabline capabilities init` writes a baseline of every grant a
repository's programs need and the most operations one run can
perform; `sabline capabilities check` derives the same from the working
tree and compares it with the baseline - with the baseline, and never
with a previous commit. A grant the baseline does not cover, a larger
count, or an effect added to a recorded function fails the check. A
missing or unreadable baseline fails rather than passes. The property:
suppose a repository's programs are held to a committed baseline by a
required check; if a change makes a program need an effect, path, host,
module or operation count the baseline does not grant, the check fails,
and it goes on failing at every later commit at which the program still
compiles and still needs it, until a person edits the baseline. However
the change is
divided among commits, the sum is reported.

This is a property of a deterministic comparison, not a detection rate.
It says nothing about intent, nothing about what a granted module does,
and nothing about code not written in Sabline.

## 4. Interoperability: a format, a corpus, an implementation

- **The format** is sabline-spec (<https://github.com/gowrishankar-infra/sabline-spec>),
  dedicated to the public domain under CC0 1.0, with JSON Schemas for
  the audit, the baseline and the in-toto predicate. It can be
  implemented without reading the compiler.
- **Three conformance levels.** L1, declaration: parse the grammar,
  compute a program's effect surface, write the audit. L2, enforcement:
  refuse at run time every operation outside the budget. L3, the
  ratchet: write and check baselines. L2 and L3 each need L1; L3 does
  not need L2, so a tool with no runtime can check baselines. No level
  needs a theorem prover.
- **A corpus of 444 JSON cases** that any implementation runs its own
  way: 298 at L1 (280 budgets to parse or refuse, 18 programs to audit),
  37 at L2 (programs run under a budget against a fixture of files and
  two local HTTP servers), 109 at L3. Thirteen scenarios are left out and
  listed with the reason - six because they depend on Python's object
  model, four because they need a Python host. The corpus is generated from the reference implementation's
  test suites and checked for drift in both repositories' CI, so the
  corpus and the implementation cannot say different things.
- **The reference implementation** is sabline-lang 5.0.0 (MIT), one
  Python file. It passes the corpus at all three levels, and its test
  suites run on every push on Linux, Windows and macOS.
- **Agent protocols.** The grammar and its covering rule - when one set
  of grants covers another - could serve as the content of a capability
  declaration on an agent tool. A draft for the Model Context Protocol
  is in sabline-spec's MCP_PROPOSAL.md; it overlaps an open proposal
  there (SEP-3140) and is written as input to it.

## 5. What has been measured

On a benchmark of 63 small programs (56 with one deliberate defect, 7
correct controls), each written in Sabline, in JavaScript for Deno and
in Python, and run by one harness under the same rules, Sabline caught
54 of the 56 defects, 42 of them before running; Deno caught 32 and
Python 28; none flagged a correct program. The benchmark was written by
the project, is small, uses inputs chosen to trigger each defect, and
was run on one machine. The ratchet has not been measured on any
repository but sabline-lang's own, nor on the gradual-attack benchmark
above, whose code is not Sabline; its test suite asserts what it
computes on scripted histories, including one where six harmless-looking
changes end in a network call three calls below `main`.

## 6. Limits

As sabline-lang's threat model states them:

- **Only code written in Sabline.** Nothing here applies to code the
  Sabline runtime does not run, and a model asked for Sabline may hand
  back something else.
- **A granted `ffi` module is trusted in full.** `ffi:os` is the
  operating system; the grant narrows which modules a call may reach,
  not what a module does.
- **Logic errors with no contract** are correct as far as the compiler
  knows.
- **The meaning of text.** A program that prints a shell command for
  its caller touches nothing; no effect system can tell it from one
  that prints the same words as a warning.
- **One maintainer.** Fixes to soundness and sandbox reports are
  promised within a week, and nothing else is promised.
- **Not a security boundary.** The budget is enforced by a Python
  interpreter in the same process as the compiler; a defective or
  altered implementation holds nothing. Side channels, resource use
  below the limits, where a granted host name resolves and what a
  granted host does with a request are outside the model. It belongs
  inside an operating-system sandbox when the stakes warrant one.
- **The ratchet's known limits,** each held as a conformance case: a
  function renamed in the same change that gives it an effect its
  program already had escapes function-level attribution; what a
  granted module does is outside the program's text; and three
  conservative false positives (a loop bound behind a call, a path
  passed as a parameter, a path written with a backslash). The ratchet
  guards nothing if the check is not required, and an edit to the
  baseline is an accepted widening whose review is the control.
- **The evaluation** is the project's own benchmark; no user study has
  been done.

## 7. What agent standards could take from this

Offered as observations from building one, not as a standard:

1. **Separate the declaration from its enforcement.** A capability
   declared by a tool or program is a claim. A standard that defines
   one should say what enforces it: the language's checker and runtime,
   the host's operating-system sandbox for a local tool, or, for a
   remote one, only whoever runs it. Signing a declaration shows who
   made it and that it has not changed, not that it is true.
2. **Compare with a declared baseline, not with the last change.** A
   check against the previous state misses capability assembled in
   small steps; a check against a baseline that only an edit can widen
   does not.
3. **Define "wider" precisely enough to test.** Interoperability comes
   from two implementations agreeing on when one set of grants covers
   another, and a shared corpus of cases is how that agreement is shown.
4. **Bind a declaration to what it describes,** by digest, so that a
   consumer can check that the declaration is of the code it is about
   to run.
5. **Measure gradual escalation.** The author knows of no benchmark
   that measures whether a repository's declared capability can widen
   unnoticed across many agent-written changes; building one would let
   approaches like this one be compared.

## Disclosure

This document was prepared with an AI coding agent (Claude Code) under
the respondent's direction, and reviewed by the respondent.

## Sources

- The paper: sabline-lang `paper/sabline.md` (draft, not yet on arXiv).
- sabline-spec SPEC.md sections 3 to 9 and CONFORMANCE.md; the corpus
  in `tests/`.
- sabline-lang THREAT_MODEL.md, `benchmark/RESULTS.md`,
  `check_ratchet.py`.
- NIST: the AI Agent Standards Initiative page above; the CAISI RFI,
  <https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents>;
  the NCCoE project,
  <https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization>;
  COSAiS, <https://csrc.nist.gov/projects/cosais>.
