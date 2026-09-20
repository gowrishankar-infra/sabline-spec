# A capability declaration for MCP tools

**Status: a draft, not sent.** Written on 2026-09-11 against the Model
Context Protocol specification revision 2026-07-28, the current one.
Nothing here has been posted to the MCP project. Released under CC0
1.0, like the rest of this repository.

## The problem

A client cannot tell, before it calls a tool, what the tool may touch.
In the 2026-07-28 schema a `Tool` has `name`, `title`, `icons`,
`description`, `inputSchema`, `outputSchema`, `annotations` and
`_meta`. The only statements about behaviour are four booleans in
`ToolAnnotations` - `readOnlyHint`, `destructiveHint`,
`idempotentHint`, `openWorldHint` - and the schema says of them: "all
properties in `ToolAnnotations` are **hints**. They are not guaranteed
to provide a faithful description of tool behavior", and "Clients
should never make tool use decisions based on `ToolAnnotations`
received from untrusted servers". Nothing names a file, a host or an
environment variable. The specification asks hosts to obtain "explicit
user consent before invoking any tool" and says "Users should
understand what each tool does before authorizing its use", but gives
the user nothing checkable to consent to.

Tool poisoning is item 3 of the OWASP MCP Top 10 (MCP03:2025, in the
list's v0.1 beta), and OWASP counts among its sub-techniques "rug pulls
(malicious updates to trusted tools)". The specification lets the tool
list change over time; nothing in it tells a client to ask again when a
tool it was allowed to call changes what it does.

## What is already proposed

This is not new ground, and it should go in as input to work already
under way rather than as a rival to it:

- **SEP-3140** (open since 2026-07-27, seeking a sponsor) proposes a
  signed capability manifest - `network`, `filesystem` read and write,
  `subprocess`, `env` - with change semantics on `list_changed` and
  runtime conformance through a sandbox or attestation. It overlaps
  this draft almost entirely.
- **SEP-1076** (dormant since 2026-01-26) proposed `network`,
  `filesystem`, `environment` and `execution` declarations on tools.
- The **Security Interest Group**'s agenda has two open items with no
  champion: "Capability declarations: hints or contracts" and "Runtime
  drift: `list_changed` semantics after approval".
- The maintainers' stated position (MCP blog, 2026-03-16): "Hints
  inform decisions; contracts enforce them. If a proposal's value
  depends on the annotation being true, it's asking for a contract, and
  the right place for that is the authorization layer, the transport,
  or the runtime rather than `ToolAnnotations`"; and, for new fields,
  "ship a namespaced field, see how it holds up in production, and come
  back with a proposal backed by actual usage".

What this draft can add to that work is not the idea but three pieces
that exist: a published grammar for scoped grants (sabline-spec
sections 4 and 5, CC0); a precise rule for when one declaration covers
another, and so for when a changed declaration is wider (section 9.5);
and a conformance corpus whose budget-grammar and covering cases
(sabline-spec `tests/`, 280 and 32 of its 444 cases) let two
implementations of the rule be checked against each other.

## The proposal

Following the maintainers' advice, a namespaced key in the tool's
`_meta` first, and a first-class field only after use:

```json
"_meta": {
  "io.github.gowrishankar-infra/capabilities": {
    "format": "sabline-spec 0.5",
    "grants": ["fs:read:./data", "net:api.example.com"],
    "counts": {"net": 100}
  }
}
```

The prefix is the reverse-DNS form of `gowrishankar-infra.github.io`,
where sabline-spec's predicate type already lives; it follows the
`_meta` key rules and is not a reserved prefix.

- `grants`, required: grants in sabline-spec's grammar, with the
  restrictions its section 9.2 puts on a baseline - no counts inside a
  grant, one module per `ffi` grant, sorted and reduced. The effects
  are `io`, `env`, `fs`, `net`, `clock`, `rand` and `ffi`; `fs` may be
  scoped to a direction and path, `net` to a host, port or one-label
  wildcard. An empty list declares that a call touches nothing outside
  the MCP exchange.
- `counts`, optional: the most `fs` and `net` operations one call may
  perform.
- `format`, required: the grammar's version.

What a declaration covers: everything a call may touch outside the
exchange itself and outside the server's own installation (its code and
the files it ships). A call's arguments and result are the exchange, so
they are not an effect. Relative paths are relative to the server
process's working directory. A path or host that the request chooses is
declared unscoped (`fs:read`, `net`), as sabline-spec 9.3 does for a
path built while running: the declaration must cover every request, not
the typical one.

A tool with no declaration has declared nothing, which is not the same
as declaring that it touches nothing.

## Two examples: sabline-lang's MCP server

sabline-lang's `sabline_mcp.py` offers four tools. Two of them, as
their `tools/list` entries would read with the key added (the
descriptions are the server's own text; `sabline_run`'s description and
input schema are shortened here):

```json
{
  "name": "sabline_card",
  "description": "The Sabline language in about 2,300 words: syntax, the rules models get wrong, every builtin with its effects and whether it can fail, full standard-library signatures, and the error table. Read this before writing Sabline.",
  "inputSchema": {"type": "object", "properties": {}},
  "_meta": {
    "io.github.gowrishankar-infra/capabilities": {
      "format": "sabline-spec 0.5",
      "grants": []
    }
  }
}
```

`sabline_card` returns `LLM.md`, a file the server ships, and touches
nothing else.

```json
{
  "name": "sabline_run",
  "description": "Run a Sabline program under an effect budget. ...",
  "inputSchema": {
    "type": "object",
    "properties": {
      "source": {"type": "string"},
      "allow": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["source"]
  },
  "_meta": {
    "io.github.gowrishankar-infra/capabilities": {
      "format": "sabline-spec 0.5",
      "grants": ["fs:read", "net:api.example.com"],
      "counts": {"net": 100}
    }
  }
}
```

That is `sabline_run` on a server its operator started with
`--max-allow io,net:api.example.com@100`. The program's output goes
into the call's result, so its `io` is part of the exchange. The `net`
grant and its count are the operator's ceiling. `fs:read` is there
because loading the program reads the files it imports, at paths the
submitted source chooses. On a server started without the flag, the
ceiling is `io` and the declaration is `["fs:read"]` alone.

The two parts of the second declaration differ in the way that matters
most. The `net` grant is enforced: the Sabline runtime refuses every
operation outside the ceiling before it happens. The `fs:read` is not:
loading happens before the budget applies, and nothing but the
server's own code limits it. Both are true today; only one of them is
held by anything.

## What a client can do with it

- **Show it before consent.** Put the grants in the consent prompt:
  "may read any file; may connect to api.example.com, at most 100 times
  a call". A user consents to something named.
- **Hold a tool to what was approved.** Keep the declaration the user
  approved for each server and tool. When a new `tools/list` arrives -
  after its `ttlMs`, or on a `list_changed` notification - compare the
  new declaration with the approved one, not with the previous list,
  using sabline-spec 9.5's covering rule: a grant the approved list
  does not cover, or a larger count, is a widening, and the client does
  not call the tool until the user approves again. Narrowing needs no
  prompt. This is the ratchet of sabline-spec 9.6 applied to tools, and
  it is aimed at the rug pull: a tool approved narrow cannot quietly
  become wide.
- **Apply a policy.** An organisation can refuse any tool that declares
  unscoped `fs:read`, or `net` outside an allow-list, before any call.

## A claim unless something enforces it

A declaration is a claim by the server. Signing it, as SEP-3140
proposes and as sabline-lang already does for its tool manifest (`sabline
mcp-verify`), proves who made the claim and that it has not changed; it
does not make the claim true. What can make it true:

- **The host, for a local server.** A host that starts a stdio server
  can run it in an operating-system sandbox built from the union of its
  tools' declarations - file-system allow-lists and network egress
  rules (Landlock, seccomp or bubblewrap on Linux, an AppContainer on
  Windows, a container with a network policy). Then a false declaration
  fails closed. This is the only enforcement a client controls.
- **The server's own runtime.** `sabline_run`'s ceiling is enforced by
  the Sabline runtime. The client has to trust the server for that, and
  sabline-lang says of itself that its budget is not a security
  boundary: it is a Python interpreter in the same process.
- **For a remote server, nothing the client can check.** An attestation
  can bind a declaration to the code deployed, and says who vouches for
  it; enforcement stays with whoever runs the server.

## What it does not solve

- **A server that lies,** where nothing enforces the declaration.
- **Poisoned descriptions.** Most of tool poisoning is instructions to
  the model hidden in a description or schema. A declaration bounds
  what a tool can touch; it says nothing about what the model is told.
- **What happens inside a grant.** A granted host receives whatever is
  sent to it; `fs:read` of a home directory includes its secrets. This
  is access, not data flow.
- **Starting processes.** sabline-spec's grammar has no effect for it.
  SEP-3140 has `subprocess`; until the grammar has one, a tool that
  starts processes can only declare unscoped `ffi`, which says
  "anything".
- **Wide declarations.** A tool whose reach depends on its arguments
  must declare the unscoped grant, as `sabline_run` does for imports.
  A narrow declaration needs a server that confines itself.
- **What a server does between calls,** such as writing its own log.

## Before sending

- Decide where it goes: most likely a comment on SEP-3140 offering the
  grammar and covering rule, or the Security Interest Group's "hints or
  contracts" item. A SEP of its own needs a sponsor, a prototype and a
  reference implementation in an official SDK.
- Build the prototype: sabline-lang's server does not emit this key
  today. It speaks protocol revision 2024-11-05 and would need updating.
- MCP's AI policy asks contributors to disclose AI assistance; this
  draft was prepared with an AI coding agent under the maintainer's
  direction, which a post or pull request should say.
