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
  this format has no counterpart to TACIT's information-flow control
  over classified data, and no grant for running commands.

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
- **How this differs:** this format tracks nothing about data - a
  budget bounds which effects, paths, hosts and modules a run may reach,
  not which values may flow to them - and its grants apply per run to
  operations, where CaMeL's policies apply per tool call to data.

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
  reference implementation gives a run with no budget all seven
  effects (SPEC.md section 4.6), so deny-by-default holds only once an
  operator writes a budget.

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
