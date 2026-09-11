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
  are unsigned, name no artifact digest, and describe what a source
  text declares rather than how or by whom an artifact was built;
  nothing here makes them attestations, and carrying an audit as an
  in-toto predicate is an open question (SPEC.md Q11).

## SARIF

OASIS. *Static Analysis Results Interchange Format (SARIF) Version
2.1.0.* OASIS Standard, 2020.

- **What it does:** a JSON format for the results of static analysis
  tools - runs, rules, and results with locations - so that one viewer
  or code-scanning service can read the output of many analysers.
- **How this differs:** `velaris.audit/1` describes a program - what
  it declares, names and promises - rather than listing findings; its
  `problems` resemble SARIF results but are not SARIF, and the
  reference implementation emits no SARIF.

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
