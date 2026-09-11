# In-toto predicate registry: the pull request, prepared

**Status, 2026-09-11: the branch is pushed; the pull request is not
open.** Three steps remain, and in-toto's rules make them the
maintainer's own (below).

- Fork: <https://github.com/gowrishankar-infra/attestation>, branch
  `velaris-capability-predicate`, commit `0f40c43`, on top of
  in-toto/attestation `main` at `2dcd055`.
- It adds `spec/predicates/velaris-capability.md`, the predicate written
  to `spec/predicates/template/template.md`, and one entry, with its link,
  in the list in `spec/predicates/README.md`. That file on the branch is
  the text to review; this file does not keep a second copy.
- in-toto's pull-request CI lints Markdown (`markdownlint-cli` 0.49.1,
  the repository's `.markdownlint.yaml`). Run over the branch, it
  reports nothing.
- No protobuf definition is included. The guidelines make one optional,
  for generated Go, Python and Java bindings; it can be added if the
  maintainers want bindings.

## What in-toto asks, as read on 2026-09-11

- `docs/new_predicate_guidelines.md`: open a pull request that follows
  the predicate template and adds the predicate to the list of existing
  predicates; the maintainers review it at their next maintainers
  meeting. A type URI outside `https://in-toto.io/attestation/` needs no
  second pull request to in-toto.io's redirects. The guidelines' four
  "preliminary questions" - the use case, why existing predicates do
  not cover it, what the predicate looks like, what policy questions it
  answers - are what a description is expected to answer.
- The in-toto contributing guidelines
  (<https://github.com/in-toto/community/blob/main/CONTRIBUTING.md>)
  require the Developer Certificate of Origin; every recent predicate
  pull request shows a `DCO` check, which fails a commit without
  `Signed-off-by`.
- in-toto's AI policy
  (<https://github.com/in-toto/community/blob/main/AI_POLICY.md>):
  - "we require users to disclose the use of AI assistance", in the pull
    request body, naming "which tool(s) have been used, how they were
    used, and ... what code or text is AI generated"; "We will reject
    any pull request that does not include the disclosure."
  - "In explaining your contribution, do not use AI to automatically
    generate comments, pull request descriptions, or issue
    descriptions."
  - "AI agents MUST NOT add Signed-off-by tags. Only humans can legally
    certify the Developer Certificate of Origin (DCO)."
  - Commits should carry `Assisted-by: AGENT_NAME:MODEL_VERSION`. The
    branch's commit carries `Assisted-by: Claude:claude-opus-5` and no
    `Signed-off-by`.
- The maintainers have closed a predicate whose intent a Simple
  Verification Result with extension fields could carry
  (in-toto/attestation#549, closed 2026-04-27). The predicate's "Why
  existing predicates do not cover them" section answers that for this
  one; a description should too.

## The three steps

1. Read `spec/predicates/velaris-capability.md` and the list entry on
   the branch; the policy asks that the submitter understand and can
   explain every line.
2. Sign off, which certifies the DCO, and push:

        cd D:\in-toto-attestation
        git commit --amend --signoff --no-edit
        git push --force-with-lease

   The clone's own `user.name` is "Palakurthi Gowri Shankar", so the
   sign-off matches the commit's author. (The global git configuration
   on this machine still says "Palakurthi Gowri shankar".)
3. Write the description yourself and open the pull request:

        gh pr create --repo in-toto/attestation --base main --head gowrishankar-infra:velaris-capability-predicate --title "Add Velaris Capability predicate type" --body-file DESCRIPTION.md

## What the description has to state

- What the predicate describes: a `velaris.audit/1` document - the
  effects a Velaris program declares, the paths, hosts and modules it
  names, bounds on its file and network operations, and the narrowest
  budget to run it under - bound by digest to the source files it
  describes.
- The use case, and why SLSA Provenance, Test Result, Simple
  Verification Result and SCAI do not cover it.
- The policy questions it answers: does the program declare `net` or
  `ffi`; does it name only allowed hosts; is the budget it needs within
  what an environment grants; did the audit compile (`ok`).
- The producer: velaris-lang 4.2.0 and later write Statements of this
  type with `velaris attest`, unsigned.
- Signing: velaris-lang's release workflow signs the Statement for
  `examples/effects.vel` with cosign and with sigstore-python, verifies
  both, and attaches the Statement and both bundles to the release.
- The command a reviewer runs (next section).
- The licence: the predicate's definition (velaris-spec SPEC.md 8.5)
  and its JSON Schema are CC0 1.0; the copy at the type URI is the same
  schema, checked by velaris-spec's `tools/check_sync.py`.
- The AI disclosure the policy requires: the tool (Claude Code, model
  claude-opus-5), how it was used (drafting the predicate text and this
  checklist, checking in-toto's rules, running the lint and the
  verification below, under the maintainer's direction), which text it
  wrote, and that the submitter reviewed it.

## For a reviewer: download and verify

With curl and cosign, from an empty directory:

    curl -sSLO https://github.com/gowrishankar-infra/velaris-lang/releases/download/v4.2.0/velaris-attestation-4.2.0.intoto.json
    curl -sSLO https://github.com/gowrishankar-infra/velaris-lang/releases/download/v4.2.0/velaris-attestation-4.2.0.cosign.sigstore.json
    curl -sSLO https://raw.githubusercontent.com/gowrishankar-infra/velaris-lang/v4.2.0/examples/effects.vel
    cosign verify-blob-attestation --bundle velaris-attestation-4.2.0.cosign.sigstore.json --type https://gowrishankar-infra.github.io/velaris-lang/capability/v1 --certificate-identity https://github.com/gowrishankar-infra/velaris-lang/.github/workflows/release.yml@refs/tags/v4.2.0 --certificate-oidc-issuer https://token.actions.githubusercontent.com effects.vel

Run on 2026-09-11 with cosign v3.0.6, it prints `Verified OK`; the
same with `4.2.1` in place of `4.2.0` does too. The first file is the
unsigned Statement, identical to velaris-spec's
[examples/capability-statement.json](examples/capability-statement.json)
and to the example in the predicate's text.

Verify against the raw file, not a checkout: the Statement's digest is
of the file's bytes as committed, with LF line endings, and a git
checkout that converts line endings (`core.autocrlf=true`, the default
on Windows, with velaris-lang's `.gitattributes` saying `* text=auto`)
gives other bytes, and cosign then reports "provided artifact digest
does not match any digest in statement".

## The type URI

It is `https://gowrishankar-infra.github.io/velaris-lang/capability/v1`,
on velaris-lang's documentation site, where it resolves to the
description and the schema. On 2026-09-11, again at the time of this
version, `velaris.dev` answered every path with a Vercel
`DEPLOYMENT_NOT_FOUND`, and nothing in either repository says who
controls that domain, so it is not used. A type URI is an identifier:
once Statements carry it, changing it is a new type. velaris-lang 4.2.0
and later write this one.
