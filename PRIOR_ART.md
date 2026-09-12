# Prior art

Published work this format sits beside. For each: what it does, and
how this format differs.

Nothing here claims the format is new. velaris-lang's changelog does
not name any of this work as the source of a design decision, and this
file does not claim one either; where a resemblance is close, it says
so and says that the record is silent about influence. The word
"capability" in "capability format" follows common usage, not the
object-capability model described first below.

## Object capabilities

Dennis, J. B. and Van Horn, E. C. "Programming Semantics for
Multiprogrammed Computations." *Communications of the ACM* 9(3),
143-155, 1966. Miller, M. S. *Robust Composition: Towards a Unified
Approach to Access Control and Concurrency Control.* PhD thesis, Johns
Hopkins University, 2006.

- **What it does:** a capability is an unforgeable reference that both
  names a resource and carries the right to use it, so authority flows
  only through what a program has been handed (Dennis and Van Horn
  introduced the term; Miller's object-capability model builds least
  authority out of it).
- **How this differs:** a Velaris effect is a name in a signature and a
  budget is ambient to the whole run - any function that declares `fs`
  may reach any path the budget allows without holding a reference to
  it - so nothing here is unforgeable and nothing is handed over.

## TACIT

Odersky, M., Zhao, Y., Xu, Y., Bračevac, O. and Pham, C. N. "Securing
Agents With Tracked Capabilities." ACM Conference on AI and Agentic
Systems (CAIS '26), 2026, doi:10.1145/3786335.3813127. Preprint as
"Tracking Capabilities for Safer Agents," arXiv:2603.00991.
Implementation: <https://github.com/lampepfl/tacit>.

- **What it does:** agents write Scala 3, compiled with capture checking
  and a safe-mode subset, in which capabilities - a file system rooted
  at a directory, a set of network hosts, a set of commands - are values
  the type system tracks, so code can use only what it was given, and
  pure sub-computations over classified data cannot leak it.
- **How this differs:** capabilities here are not values in a type
  system but effect names in signatures plus an operator's budget
  written as text and enforced by the interpreter at each operation,
  in a small language a model learns from a card rather than Scala 3;
  and there is no grant for running commands.

  On information-flow control this file said, until 0.7, that the
  format had no counterpart at all. That was true until velaris-lang
  6.0 (2026-09-12), which added `Secret of T`: `env()` and
  `read_file_secret()` return one, no builtin that declares an effect
  accepts an argument carrying one, a list, map or record holding one
  carries it, and `declassify(value, reason)` is the only way out -
  itself an effect, so it appears in a signature, in this format's
  `effects`, in the budget an operator writes, and in the audit's
  `secrets` section with the reason written in the call. SPEC.md
  section 3.1 of velaris-lang states it; section 8.6 here states what
  the audit reports.

  What TACIT still has that this does not: its capture checking tracks
  *every* value's captured capabilities as part of the type, where
  Velaris marks the results of two builtins and nothing else - a
  secret that reaches a program through standard input, its arguments,
  the network or the host language is an ordinary `Text`, and a
  program cannot mark one itself. Velaris bounds explicit flow only:
  a comparison over a secret yields an ordinary `Bool`, deliberately,
  so a program may learn a secret through its own control flow and
  then print what it learned. Neither is a non-interference result,
  but TACIT's is the stronger of the two, and it is checked over Scala
  3's whole type system rather than over one wrapper type.

## CaMeL

Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N.,
Fabian, D., Kern, C., Shi, C., Terzis, A. and Tramèr, F. "Defeating
Prompt Injections by Design." arXiv:2503.18813, 2025.

- **What it does:** a privileged model turns the trusted user request
  into a program in a restricted subset of Python, run by a custom
  interpreter; a quarantined model with no tools parses untrusted data;
  every value carries capabilities - its provenance and its allowed
  readers - and security policies are checked when a tool is called, so
  untrusted data cannot change the control flow or leave through a flow
  the policy forbids.
- **How this differs:** a budget bounds which effects, paths, hosts and
  modules a run may reach, not which values may flow to them, and its
  grants apply per run to operations where CaMeL's policies apply per
  tool call to data. Until 0.7 this file said the format tracked
  nothing about data at all; from velaris-lang 6.0 it tracks one thing,
  `Secret of T` (section 3.1 there, section 8.6 here). The difference
  that remains is the one that matters: CaMeL tags *every* value with
  its provenance and its permitted readers, computed as the program
  runs, and checks a policy at each tool call; Velaris marks the
  results of two builtins at compile time, has no notion of provenance
  or of a reader, and lets a comparison over a marked value give an
  ordinary Bool. CaMeL's design is aimed at untrusted *data* changing
  what a program does; nothing here addresses that.

## WASI

WebAssembly System Interface, WebAssembly Community Group,
<https://wasi.dev> (Preview 1, and Preview 2 on the Component Model).

- **What it does:** system interfaces for WebAssembly with no ambient
  authority: a module can reach only the directories, sockets and other
  resources its host hands it as handles, so a module given nothing can
  reach nothing.
- **How this differs:** grants here are text an operator writes, not
  handles passed to the program; they are enforced by an interpreter in
  the same process, not at a virtual machine's boundary; and the
  reference implementation gives a run with no budget `io` - the
  console and nothing else (SPEC.md section 4.6). Until velaris-lang
  5.0 (2026-09-12) it gave all seven effects, and this paragraph said
  that deny-by-default held only once an operator wrote a budget. That
  was true until 5.0; what remains is that a program given nothing can
  still print, where a WASI module given nothing cannot.

## in-toto and SLSA

Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R. and
Cappos, J. "in-toto: Providing farm-to-table guarantees for bits and
bytes." USENIX Security 2019; the in-toto Attestation Framework,
<https://github.com/in-toto/attestation>. SLSA, Supply-chain Levels for
Software Artifacts, <https://slsa.dev>, and its provenance predicate.

- **What they do:** signed statements about software artifacts - an
  in-toto attestation binds a typed predicate to subjects identified by
  digest, and SLSA defines levels of build integrity and a provenance
  predicate that records how an artifact was built.
- **How this differs:** `velaris.audit/1` and `velaris.capabilities/1`
  describe what a source text declares rather than how or by whom an
  artifact was built, and on their own they are unsigned and name no
  artifact digest. From 0.4, SPEC.md section 8.5 defines an in-toto
  predicate type that carries an audit with the digests of the files
  audited; in-toto supplies the Statement, the envelope and the
  signing, and this format only the predicate. SLSA has no counterpart
  here: nothing in this format says how an artifact was built. From
  velaris-lang 4.2.0 the reference implementation writes Statements of
  the type (`velaris attest`) and leaves signing to Sigstore's tools,
  cosign and sigstore-python; until 0.5 this file said it wrote none,
  which was true of 4.1.0.

## SARIF

OASIS. *Static Analysis Results Interchange Format (SARIF) Version
2.1.0.* OASIS Standard, 2020.

- **What it does:** a JSON format for the results of static analysis
  tools - runs, rules, and results with locations - so that one viewer
  or code-scanning service can read the output of many analysers.
- **How this differs:** `velaris.audit/1` describes a program - what
  it declares, names and promises - rather than listing findings; its
  `problems` resemble SARIF results but are not SARIF. SARIF is not
  part of this format. The reference implementation also writes its
  findings as SARIF 2.1.0, from velaris-lang 3.4; until 0.4 this file
  said it emitted none, which was true of 3.1.1, the version it was
  first written against.

## Distributed attacks in persistent-state AI control

Hills, J., Caspary, I. and Cooper Stickland, A. "Distributed Attacks in
Persistent-State AI Control." arXiv:2607.02514, 2026.

- **What it does:** introduces Iterative VibeCoding, a setting in which
  a coding agent builds software over a sequence of pull requests in a
  persistent codebase while pursuing a covert side task, and compares
  gradual attacks, which spread the side task across pull requests,
  with attacks concentrated in one. It reports that no single monitor
  it tested is robust to both, that gradual attacks evade diff monitors
  at high rates, and that a stateful monitor tracking suspicious
  buildup across pull requests detects them better.
- **How this differs:** the capability ratchet of section 9 is not a
  monitor of intent. It is a deterministic comparison of what a
  repository's Velaris programs need - effects, paths, hosts, modules,
  operation counts, each function's effects - with a baseline the
  repository declared, at every change and never against the change
  before. It sees the part of a gradual attack that needs capability
  the baseline did not declare, and nothing else: a side task that
  stays inside the declared surface, or is not written in Velaris, is
  outside it. It has not been measured on that paper's benchmark. The
  record does not say the paper influenced the ratchet, which shipped
  in velaris-lang 4.0.0 after it was posted.

## The AI-first language field

Allan, A., ed. *Agent Languages*, <https://agentlanguages.dev>,
mirrored at
<https://research.tedneward.com/places/agentlanguages.html>. Read at
the version of 11 September 2026, when it tracked 41 projects; the
framing essay is "Three Camps, Alike in Dignity,"
<https://negroniventurestudios.com/2026/05/20/three-camps-alike-in-dignity/>.
Catalogue text is CC BY 4.0.

A catalogue of languages designed for models rather than for people now
exists, and it sorts them into three camps that disagree about what the
problem is: **Syntactic**, which strips ambiguity at the token level;
**Verification**, which makes contracts mechanically checkable; and
**Orchestration**, which treats the matter as agent coordination rather
than as a language problem. Velaris belongs in Verification and
Orchestration - contracts a prover discharges, and effects and budgets
gating what a run may do. Velaris is not in the catalogue; this section
was written before submitting it, and the entries below were read at
their own repositories and not only in the catalogue.

Nothing in this field is cited by velaris-lang, and the record does not
say that any of it influenced the design. The honest summary is that
the field has converged, independently and in public, on most of what
Velaris does. Effects declared in signatures; a prover with a runtime
fallback where it cannot settle an obligation; a machine-readable
record of what was checked; a policy an operator writes and a runtime
enforces - each of these appears in projects listed below, several of
them older than the Velaris release that first shipped it. What the
catalogue does not show is one project combining all four.

**Boruna.** <https://github.com/escapeboy/boruna>, MIT, Rust, working;
v3.2.0 at reading, though the catalogue's entry still records v0.2.0
and 34 commits. Orchestration and Verification.

- **What it does:** a deterministic, capability-safe language (`.ax`)
  and workflow engine for auditable AI systems. A function declares its
  side effects in a `!{net.fetch, fs.write}` clause after the return
  type, drawn from a fixed set of eleven capabilities; a VM capability
  gateway checks every call against an operator's policy, which can
  restrict capabilities, reachable endpoints, invocable models, and
  token and call budgets per step. `requires` preconditions are
  enforced at run time and trap with a reproducible counterexample, and
  a function may declare an `intent` string captured into the evidence
  record. Runs produce hash-chained tamper-evident evidence bundles -
  SHA-256 chained from a genesis entry holding the workflow definition
  hash, so that altering an entry breaks the chain - covering inputs,
  outputs, model responses, policy decisions and approvals, verifiable
  offline with `boruna evidence verify`; a recorded workflow replays to
  identical outputs. Four versioned specifications, an MCP server, and
  a stability policy with dated support windows.
- **How this differs:** this is the closest work to Velaris in the
  catalogue, and on the runtime and provenance side it is not
  meaningfully behind. Three differences are real. Boruna parses
  `ensures` but does not enforce it and integrates no prover, where
  Velaris discharges contracts with Z3 and checks at run time only what
  the prover could not settle. Boruna's evidence describes a run - what
  executed, and what the model returned - where `velaris.audit/1`
  describes a source text's declared surface without running it, and
  velaris-spec binds that to existing supply-chain infrastructure
  through an in-toto predicate type and writes findings as SARIF, which
  Boruna does neither of; Boruna's bundles are checksummed but not yet
  signed, which its own documentation records as an open gap. Velaris
  has nothing answering to Boruna's deterministic replay, approval
  gates or envelope encryption. On deny-by-default Boruna is still the
  stricter of the two, but by much less than this entry first said.
  Its default policy grants nothing. Until velaris-lang 5.0
  (2026-09-12) a Velaris run with no budget got all seven effects, and
  this paragraph said so; from 5.0 it gets `io` - print, read a line,
  and the command-line arguments - and every other effect is refused
  (SPEC.md section 4.6). So the gap is now one effect, not seven: a
  Velaris program given no budget can write to the console, and a
  Boruna one cannot.

**Thermite.** <https://github.com/dollspace-gay/Thermite>, MIT, Rust
and Lean 4, working. Verification, listed as also spanning
Orchestration.

- **What it does:** every function declares `req`, `ens` and `fx`
  clauses - precondition, postcondition and permitted effects, the last
  checked for subsumption up the call graph - and the Forge driver
  settles each obligation separately on a five-rung assurance ladder:
  L4 reconstruction in Lean with LRAT proof replay, L3 an all-input
  proof through Verus or Z3, L2 bounded model checking with the bound
  recorded, L1 an always-active runtime contract check, L0 an explicit
  trust escape. A counterexample is a failure and never a downgrade.
  The per-clause assurance manifest records which engine settled each
  obligation and at what level, `forge audit` re-derives the recorded
  trust chain, and a hosted executable is confined by a seccomp filter
  derived from its `fx` clauses. Mutation testing checks contracts for
  vacuity; there is a conformance directory with certificate oracles.
- **How this differs:** of everything here this is nearest to the whole
  of what Velaris does - contracts, a prover, effects, a runtime check
  where the proof does not reach, and a machine-readable record of what
  was checked - and on verification it is well ahead: three engines, a
  graded ladder, proof reconstruction and vacuity testing, against
  Velaris's single Z3 tier. The difference worth stating is who writes
  the policy. Thermite's confinement is derived from the program's own
  `fx` clauses, so an operator cannot narrow it without editing the
  program; a Velaris budget is written by the operator, may be narrower
  than what the program declares, and is refused against at each
  operation. Thermite's manifest is a verification report about
  obligations; `velaris.audit/1` is a description of a program's
  declared capability surface, published as a separate format with a
  conformance corpus and an in-toto predicate type. Velaris has no
  counterpart to proof reconstruction or to the assurance ladder.

**Vera.** <https://github.com/aallan/vera>, MIT, Python, working,
v0.1.13 at reading. Verification, also spanning Orchestration; written
by the catalogue's own editor.

- **What it does:** mandatory `requires`, `ensures` and `effects`
  clauses on every function, with no opt-out, sorted into three tiers -
  Z3's decidable fragment on a ten-second budget, Z3 with hints
  (specified, not implemented), and compiled runtime guards for what
  neither settles - with `vera verify --json` reporting which
  obligation landed in which tier. Ten effects, including `Inference`
  for model calls as a typed algebraic effect and a `DB` effect that
  requires literal query provenance, so that string-assembled SQL is a
  compile error. Parameters are referenced by type and binding depth
  (`@Int.0`) rather than by name. 244 conformance programs and a
  fourteen-chapter draft specification.
- **How this differs:** the verification design is close enough to
  Velaris's to be worth stating plainly - mandatory contracts, a
  prover, a runtime guard where the prover does not reach, a
  conformance corpus, a written specification - and Vera reached it
  independently. Velaris's separable part is the operator's budget:
  Vera's effects are declared and checked, but its README describes no
  budget an operator writes to bound which paths, hosts or modules a
  run may reach, no refusal at the operation, and no audit, provenance
  or attestation record. Velaris has no counterpart to Vera's
  information-flow rule for SQL.

**AILANG.** <https://github.com/sunholo-data/ailang>, Apache-2.0, Go,
working, v0.20.1. Verification.

- **What it does:** row-polymorphic Hindley-Milner inference with
  effects declared in signatures as effect rows (`! {IO, FS}`) over
  five capability categories - IO, FS, Net, Clock, AI - granted at the
  command line with `--caps` and not wideable from inside the program,
  with per-effect traces and deterministic replay.
- **How this differs:** effects in the signature plus a grant the
  operator passes at the command line is Velaris's arrangement, arrived
  at separately. AILANG's grants are whole categories, where a Velaris
  grant is scoped to paths, hosts, modules and operation counts; and
  AILANG has no contracts, no prover, and no audit or attestation
  record.

**Mog.** <https://github.com/voltropy/mog>, MIT, Rust, working.
Syntactic.

- **What it does:** a script declares `requires` or `optional` for
  capabilities (fs, http, log) and the host grants them in a `.mogdecl`
  declaration; the runtime refuses a call to anything unregistered, and
  there is no ambient authority.
- **How this differs:** the same shape of declaration plus host grant,
  at the granularity of the capability rather than of the resource. No
  contracts, no prover, no record; the project describes its own
  security model as unaudited.

**Hale.** <https://github.com/hale-lang/hale>, Apache-2.0, working,
v0.16.0. Verification.

- **What it does:** compile-time effect certificates - `@no_syscall`,
  `@deterministic`, `@budget`, `@effects(only: ...)` - proven
  transitively through helpers and imported libraries with no runtime
  cost, above which sit named architectural claims over the program's
  locus graph (`forbid reaches(A, B)`, `count publishers(topic T) <=
  1`), rejected rather than guessed at wherever the graph will not
  resolve statically. Machine-readable topology artifacts can be
  versioned, re-checked in CI and diffed to track architectural change;
  binaries are attested with ES256 signatures over artifact bytes.
- **How this differs:** the versioned, diffable topology artifact
  checked in CI is the nearest thing in the catalogue to the capability
  ratchet of section 9, and is recorded here as such, though it tracks
  a locus graph rather than a capability surface, and the record does
  not describe a baseline that a change must not exceed. Hale's
  guarantees are static and lower to no runtime code, where Velaris
  refuses at the operation. Hale signs artifacts but does not use
  in-toto.

**Contracts and provers, without a budget.** Several projects mandate
contracts and discharge them mechanically, with no operator-written
grant and no provenance record. **Intent**
(<https://github.com/lhaig/intent>, Apache-2.0, Go) makes
`requires`/`ensures`/`invariant` the product and the generated code the
derivative, discharges them with Z3, and lowers what it cannot prove to
runtime checks that behave identically across Rust, JavaScript and
WebAssembly. **Vow** (<https://github.com/vow-lang/vow>, MIT,
self-hosted) lowers contracts to ESBMC bounded model checking and
returns counterexamples as re-runnable inputs, with blame attributed to
caller or callee, sound only within its unwinding bounds. **NanoLang**
(<https://github.com/jordanhubbard/nanolang>, Apache-2.0, C) requires a
shadow test block on every function and proves its core in Coq - 193
theorems, no axioms, no `Admitted` - while documenting plainly that
effects, async, the FFI and the VM lie outside the proved fragment.
**Prove** (code.botwork.se, source under a licence forbidding use as
training data) pairs refinement types and hard postconditions with
refutation challenges that require the author to say why a plausible
mutation is wrong. Velaris differs from all four in the same way: they
verify a program, and none of them bounds what a run may reach, records
what it declared, or refuses an operation.

**Further from Velaris.** **Pact**
(<https://github.com/KikotVit/pact-lang>, MIT) puts intent, effects
(`needs db, time, rng`) and errors in the signature and swaps effect
implementations for deterministic tests, with no prover. **Lumen**
(<https://github.com/alliecatowo/lumen>, MIT) has algebraic effects
with handlers and writes policy into the source as grants (`grant Chat
max_tokens 1024`) rather than into configuration - the opposite of
Velaris's division, in which the grant is the operator's and sits
outside the program - with no audit record. **Zero** (Vercel Labs,
<https://github.com/vercel-labs/zerolang>, Apache-2.0, early) passes
capability objects explicitly into `main` and puts its effort into
stable error codes and typed repair plans as JSON. **MoonBit**
(<https://www.moonbitlang.com>, the most mature entry in the
catalogue) has conventional effect typing and prunes ill-typed
continuations during generation with a semantics-aware sampler.
**Quasar** (arXiv:2506.12202, University of Pennsylvania) is
paper-only: it transpiles a Python subset and infers user-approval
gates for sensitive operations by static analysis, with
conformal-prediction reliability bounds. **Tacit**
(<https://github.com/weetster/tacit>, Apache-2.0 or MIT) makes a
BLAKE3 content-addressed AST the source of truth, with mandatory effect
rows at unit boundaries; this is a different project from the TACIT
capability-tracking work cited above, by a different author, and the
two should not be conflated.

## Also close

These two are not cited by velaris-lang, and are listed because the
resemblance is close enough that leaving them out would read as a claim.

**Deno's permissions.** <https://docs.deno.com/runtime/fundamentals/security/>

- **What it does:** a JavaScript and TypeScript runtime that gives a
  script no file, network, environment or subprocess access unless
  flags grant it, and the flags can be scoped:
  `--allow-read=<paths>`, `--allow-net=<host:port>`,
  `--allow-env=<names>`.
- **How this differs:** the grant grammar here has much the same shape,
  and velaris-lang's benchmark compares the two directly, but the record
  does not say whether Deno's flags influenced it; a Deno permission
  denial is an exception a script can catch, while a refusal here ends
  the run (SPEC.md G3), and this format scopes neither environment
  variables by name nor processes by command.

**Effect systems.** Lucassen, J. M. and Gifford, D. K. "Polymorphic
Effect Systems." POPL 1988, 47-57.

- **What it does:** extends a type system so that the type of an
  expression records the side effects evaluating it may have, checked
  statically, with effects that can be polymorphic over the functions a
  function is given.
- **How this differs:** `uses` is a fixed set of seven effect names with
  no polymorphism - a function value is simply required to be pure
  (SPEC.md T4) - which makes the static rule a small instance of the
  idea; the record does not say whether this line of work influenced
  it.
