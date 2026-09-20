# Prior art

Published work this format sits beside. For each: what it does, and
how this format differs.

Nothing here claims the format is new. sabline-lang's changelog does
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
- **How this differs:** a Sabline effect is a name in a signature and a
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
  format had no counterpart at all. That was true until sabline-lang
  6.0 (2026-09-12), which added `Secret of T`: `env()` and
  `read_file_secret()` return one, no builtin that declares an effect
  accepts an argument carrying one, a list, map or record holding one
  carries it, and `declassify(value, reason)` is the only way out -
  itself an effect, so it appears in a signature, in this format's
  `effects`, in the budget an operator writes, and in the audit's
  `secrets` section with the reason written in the call. SPEC.md
  section 3.1 of sabline-lang states it; section 8.6 here states what
  the audit reports.

  What TACIT still has that this does not: its capture checking tracks
  *every* value's captured capabilities as part of the type, where
  Sabline marks the results of two builtins and nothing else - a
  secret that reaches a program through standard input, its arguments,
  the network or the host language is an ordinary `Text`, and a
  program cannot mark one itself. Sabline also has no generic code
  over secrets unless a signature says `Secret of T` explicitly, where
  TACIT's checking follows capabilities through polymorphism. Neither
  is a non-interference result: sabline-lang 7.0.0 bounds what a
  program can do with a secret's value and says nothing about how long
  it runs or whether it stops. TACIT's is the stronger of the two, and
  it is checked over Scala 3's whole type system rather than over one
  wrapper type.

  sabline-lang 6.0.0, published for one day, let a comparison over a
  secret give an ordinary boolean, which made the whole type a
  decoration - a loop of comparisons reads the value out. 7.0.0 closed
  that. This paragraph records it because the entry would otherwise
  read as though the comparison had been thought through from the
  start; it had not.

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
  nothing about data at all; from sabline-lang 6.0 it tracks one thing,
  `Secret of T` (section 3.1 there, section 8.6 here). The difference
  that remains is the one that matters: CaMeL tags *every* value with
  its provenance and its permitted readers, computed as the program
  runs, and checks a policy at each tool call; Sabline marks the
  results of two builtins at compile time and has no notion of
  provenance or of a reader. CaMeL's design is aimed at untrusted *data* changing
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
  console and nothing else (SPEC.md section 4.6). Until sabline-lang
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
- **How this differs:** `sabline.audit/1` and `sabline.capabilities/1`
  describe what a source text declares rather than how or by whom an
  artifact was built, and on their own they are unsigned and name no
  artifact digest. From 0.4, SPEC.md section 8.5 defines an in-toto
  predicate type that carries an audit with the digests of the files
  audited; in-toto supplies the Statement, the envelope and the
  signing, and this format only the predicate. SLSA has no counterpart
  here: nothing in this format says how an artifact was built. From
  sabline-lang 4.2.0 the reference implementation writes Statements of
  the type (`sabline attest`) and leaves signing to Sigstore's tools,
  cosign and sigstore-python; until 0.5 this file said it wrote none,
  which was true of 4.1.0.

## SARIF

OASIS. *Static Analysis Results Interchange Format (SARIF) Version
2.1.0.* OASIS Standard, 2020.

- **What it does:** a JSON format for the results of static analysis
  tools - runs, rules, and results with locations - so that one viewer
  or code-scanning service can read the output of many analysers.
- **How this differs:** `sabline.audit/1` describes a program - what
  it declares, names and promises - rather than listing findings; its
  `problems` resemble SARIF results but are not SARIF. SARIF is not
  part of this format. The reference implementation also writes its
  findings as SARIF 2.1.0, from sabline-lang 3.4; until 0.4 this file
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
  repository's Sabline programs need - effects, paths, hosts, modules,
  operation counts, each function's effects - with a baseline the
  repository declared, at every change and never against the change
  before. It sees the part of a gradual attack that needs capability
  the baseline did not declare, and nothing else: a side task that
  stays inside the declared surface, or is not written in Sabline, is
  outside it. It has not been measured on that paper's benchmark. The
  record does not say the paper influenced the ratchet, which shipped
  in sabline-lang 4.0.0 after it was posted.

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
than as a language problem. Sabline belongs in Verification and
Orchestration - contracts a prover discharges, and effects and budgets
gating what a run may do. Sabline is not in the catalogue; this section
was written before submitting it, and the entries below were read at
their own repositories and not only in the catalogue.

Nothing in this field is cited by sabline-lang, and the record does not
say that any of it influenced the design. The honest summary is that
the field has converged, independently and in public, on most of what
Sabline does. Effects declared in signatures; a prover with a runtime
fallback where it cannot settle an obligation; a machine-readable
record of what was checked; a policy an operator writes and a runtime
enforces - each of these appears in projects listed below, several of
them older than the Sabline release that first shipped it. What the
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
- **How this differs:** this is the closest work to Sabline in the
  catalogue, and on the runtime and provenance side it is not
  meaningfully behind. Three differences are real. Boruna parses
  `ensures` but does not enforce it and integrates no prover, where
  Sabline discharges contracts with Z3 and checks at run time only what
  the prover could not settle. Boruna's evidence describes a run - what
  executed, and what the model returned - where `sabline.audit/1`
  describes a source text's declared surface without running it, and
  sabline-spec binds that to existing supply-chain infrastructure
  through an in-toto predicate type and writes findings as SARIF, which
  Boruna does neither of; Boruna's bundles are checksummed but not yet
  signed, which its own documentation records as an open gap. Sabline
  has nothing answering to Boruna's deterministic replay, approval
  gates or envelope encryption. On deny-by-default Boruna is still the
  stricter of the two, but by much less than this entry first said.
  Its default policy grants nothing. Until sabline-lang 5.0
  (2026-09-12) a Sabline run with no budget got all seven effects, and
  this paragraph said so; from 5.0 it gets `io` - print, read a line,
  and the command-line arguments - and every other effect is refused
  (SPEC.md section 4.6). So the gap is now one effect, not seven: a
  Sabline program given no budget can write to the console, and a
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
  of what Sabline does - contracts, a prover, effects, a runtime check
  where the proof does not reach, and a machine-readable record of what
  was checked - and on verification it is well ahead: three engines, a
  graded ladder, proof reconstruction and vacuity testing, against
  Sabline's single Z3 tier. The difference worth stating is who writes
  the policy. Thermite's confinement is derived from the program's own
  `fx` clauses, so an operator cannot narrow it without editing the
  program; a Sabline budget is written by the operator, may be narrower
  than what the program declares, and is refused against at each
  operation. Thermite's manifest is a verification report about
  obligations; `sabline.audit/1` is a description of a program's
  declared capability surface, published as a separate format with a
  conformance corpus and an in-toto predicate type. Sabline has no
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
  Sabline's to be worth stating plainly - mandatory contracts, a
  prover, a runtime guard where the prover does not reach, a
  conformance corpus, a written specification - and Vera reached it
  independently. Sabline's separable part is the operator's budget:
  Vera's effects are declared and checked, but its README describes no
  budget an operator writes to bound which paths, hosts or modules a
  run may reach, no refusal at the operation, and no audit, provenance
  or attestation record. Sabline has no counterpart to Vera's
  information-flow rule for SQL.

**AILANG.** <https://github.com/sunholo-data/ailang>, Apache-2.0, Go,
working, v0.20.1. Verification.

- **What it does:** row-polymorphic Hindley-Milner inference with
  effects declared in signatures as effect rows (`! {IO, FS}`) over
  five capability categories - IO, FS, Net, Clock, AI - granted at the
  command line with `--caps` and not wideable from inside the program,
  with per-effect traces and deterministic replay.
- **How this differs:** effects in the signature plus a grant the
  operator passes at the command line is Sabline's arrangement, arrived
  at separately. AILANG's grants are whole categories, where a Sabline
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
  guarantees are static and lower to no runtime code, where Sabline
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
mutation is wrong. Sabline differs from all four in the same way: they
verify a program, and none of them bounds what a run may reach, records
what it declared, or refuses an operation.

**Further from Sabline.** **Pact**
(<https://github.com/KikotVit/pact-lang>, MIT) puts intent, effects
(`needs db, time, rng`) and errors in the signature and swaps effect
implementations for deterministic tests, with no prover. **Lumen**
(<https://github.com/alliecatowo/lumen>, MIT) has algebraic effects
with handlers and writes policy into the source as grants (`grant Chat
max_tokens 1024`) rather than into configuration - the opposite of
Sabline's division, in which the grant is the operator's and sits
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

## Agents as operating systems

Pirch, L., Horlboge, M., Großmann, P., Asif, S. M., Kireev, K., Holz, T.
and Rieck, K. "Toward Securing AI Agents Like Operating Systems."
arXiv:2605.14932, 14 May 2026 (under submission).

- **What it does:** reads an LLM agent as an operating system and carries
  OS security mechanisms across. Its Table I maps the LLM to the *user* -
  "an untrusted actor whose actions must be mediated" - the agent runtime
  to the kernel, tools to system calls, skills to programs, the context to
  memory, files to storage and the gateway to the network. From that it
  argues for process isolation, sandboxing, "permission declarations and
  runtime enforcement", interface filtering and a minimal trusted computing
  base, notes that a "declarative skill format or a constrained tool
  language can make it easier to analyze requested permissions and harder
  to hide arbitrary behavior", and finds that of the agents it tested one
  resisted seven attacks where a baseline resisted none. It observes that
  fine-grained permission control "remains uncommon in practice".
- **How this differs:** the analogy fits Sabline more than most - the
  interpreter is the kernel, the effect-declaring builtins are classes of
  system call, and the budget is the permission set enforced at each call.
  Two things do not map. The paper's untrusted principal issues calls one
  turn at a time, and its table has no step for reading a whole program
  *before* it runs, which is what `sabline.audit/1` is; and the paper wants
  permissions per skill or tool, where a Sabline budget covers the whole
  run. The paper has no counterpart to a baseline a change must not exceed
  (the ratchet), and Sabline none to its process isolation between skills
  or to separating instructions from data in the context. The record does
  not say the paper influenced the design, which predates it.

## Authorization decided outside the program

**aiAuthZ.** Kodathala, S. V. "aiAuthZ: Off-Host, Identity-Bound
Authorization for AI Agents." arXiv:2607.05518, 6 July 2026 (technical
report).

- **What it does:** a gateway on infrastructure the agent holds no
  credentials for decides each tool call as it happens. It checks a
  per-message HMAC-SHA256 signature binding the call to a user, session,
  message and single-use nonce; then a role policy; then an argument policy
  the agent can neither read nor change - path and URL allow/deny lists,
  recipient allowlists, per-tool rate limits, written as YAML with user
  policy over workspace; and it hash-chains every decision. It reports 0%
  attack success across fifteen models with the gateway in place, at under
  0.03 ms a decision.
- **How this differs:** aiAuthZ's argument rules resemble a Sabline
  budget's paths, hosts and counts, but it binds each decision to a
  verified human identity and runs *outside* the agent's host, deciding at
  the call. Sabline knows no identity, enforces in the same process as the
  program, and describes a program before it runs rather than logging
  decisions after. The two are complementary: a gateway of this shape could
  sit in front of a host that runs Sabline.

**The agents.txt draft.** Dutta, S. "AGENTS.TXT: Strict Policy File for
Automated Clients." `draft-srijal-agents-policy-00`, an individual IETF
Internet-Draft, 7 October 2025 (expired 10 April 2026).

- **What it does:** a plain-text file at `/agents.txt` in which a *site*
  lists paths an automated client may or may not reach (`/status ALLOW`,
  `/admin DISALLOW`, optional `key=value` parameters), with a SHA-256 on
  its first line so that a malformed or altered file "MUST result in
  treating the entire site as restricted".
- **How this differs:** the direction is opposite. agents.txt is a site
  declaring, to clients it does not control, what they may do to it; a
  Sabline budget is written by whoever runs a program, about what that run
  may reach, and the interpreter enforces it against the program regardless
  of what the program says. One is a request a well-behaved client honours;
  the other is a guard the runtime imposes.

## Embedded scripting

Languages embedded in a host application, which bound a script by what the
host exposes rather than by what the script declares. Listed because the
comparison is often drawn, and the difference is the same in each case.

- **Starlark** (Bazel, <https://github.com/bazelbuild/starlark>): "By
  default, user code cannot interact with the environment"; deterministic
  and hermetic, values freeze, recursion is an error, loops are finite. The
  host predeclares any builtins a script may call.
- **Rhai** (<https://rhai.rs>): "sand-boxed so a script can never read from
  outside its own environment"; the host registers the Rust functions a
  script may call, and limits are counts - call depth, string and array
  size, `max_operations`.
- **Luau** (<https://luau.org>): the `io` library "has been removed
  entirely", most of `os`, `package` and `debug` with it; globals are
  read-only; an interrupt handler stops a long run. Its gradual type
  checker gives warnings, not a security boundary.
- **Shopify Functions** (<https://shopify.dev/docs/apps/build/functions>):
  a WebAssembly module whose input is fixed by a GraphQL query you define,
  with an instruction limit (11 million) and no clock or randomness; some
  functions may make one host-mediated `fetch` the platform performs.
- **V8 isolates** (Cloudflare Workers, Deno Subhosting): tenants are
  isolated in V8, the platform's own APIs and bindings define what code can
  reach, no filesystem, CPU and memory bounded.

**How this differs:** in all of them the grant is *the set of functions the
host provides*, and the script declares nothing about what it will use.
Sabline inverts both halves: each function declares its effects in its
signature, checked statically up the call graph; the operator's budget
scopes those effects to paths, hosts, modules and counts and is refused
against at each operation; and `sabline.audit/1` reports both from the
source before anything runs. None of these embeds a prover or a written
capability record.

## Code mode

An agent writes a program that calls tools, instead of emitting tool calls
one at a time. The question this format asks of each is what can be said
about the code *before* it runs.

- **Cloudflare Code Mode** (<https://blog.cloudflare.com/code-mode/>, Sept
  2025): an MCP server's schema becomes a TypeScript API the model writes
  against, run in a Worker isolate where "the global `fetch()` and
  `connect()` functions throw errors" and bindings supply already-authorized
  clients. Before running, what is known is which MCP servers are bound -
  not which tools the code will call, and no analysis of the code is
  described.
- **Anthropic programmatic tool calling**
  (<https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling>):
  Claude writes Python in a container where tools appear as functions; each
  call is returned to the client to run, and `allowed_callers` marks which
  tools code may call - but the documentation says it "is not a hard
  API-level block ... Do not rely on `allowed_callers` as a security
  boundary." Known before running: which tools were offered to the code.
- **Mastra** (<https://mastra.ai/docs/agents/code-mode>) and **TanStack AI**
  (<https://tanstack.com/ai/latest/docs/code-mode/code-mode>): the model
  writes TypeScript that calls tools as `external_*` / typed stubs, run in
  a sandbox or isolate; TanStack strips the types with sucrase and does not
  check them, and lists no pre-run analysis of the code.
- **Strands Agents** (<https://strandsagents.com>): the SDK's sandbox runs
  shell commands and code (`sandbox_shell`, `Sandbox.execute_code`) but, as
  documented, does not expose the agent's tools to that code; the community
  `strands-code-agent` does, bounded by an import allowlist.

**How this differs:** each of these knows, at most, which tools the code
was *offered* before it runs, and nothing about what the code will do with
them; none describes checking the code, and Anthropic's own docs say its
caller restriction is not a boundary. Sabline reads the program first and
reports which effects, paths, hosts and modules each function needs, and
the runtime refuses anything outside the budget. Its "code" is a small
language with a prover, not a general-purpose host language in a sandbox,
which is the trade: less expressive, more that can be said before it runs.

## Also close

These two are not cited by sabline-lang, and are listed because the
resemblance is close enough that leaving them out would read as a claim.

**Deno's permissions.** <https://docs.deno.com/runtime/fundamentals/security/>

- **What it does:** a JavaScript and TypeScript runtime that gives a
  script no file, network, environment or subprocess access unless
  flags grant it, and the flags can be scoped:
  `--allow-read=<paths>`, `--allow-net=<host:port>`,
  `--allow-env=<names>`.
- **How this differs:** the grant grammar here has much the same shape,
  and sabline-lang's benchmark compares the two directly, but the record
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
