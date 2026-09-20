#!/usr/bin/env python3
"""Check the schemas, the examples, and the conformance corpus.

usage: python tools/validate.py [--audits DIR] [--capabilities FILE]

- every file in schemas/ must be a valid JSON Schema (draft 2020-12);
- every examples/**/*.audit.json must validate as velaris.audit/1;
- every examples/*statement.json must be an in-toto Statement v1 of the
  capability/v1 predicate type (SPEC.md 8.5), its predicate valid
  against schemas/capability-predicate.v1.schema.json and its audit
  against the velaris.audit/1 schema;
- every examples/*receipt.json must be an in-toto Statement v1 of the
  receipt/v1 predicate type (SPEC.md 8.7), its predicate valid against
  schemas/receipt-predicate.v1.schema.json, and there must be one;
- every examples/*.capabilities.json must validate as
  velaris.capabilities/1, with its programs sorted by file and unique,
  and every grant list sorted and reduced - rules of SPEC.md section
  9.2 that JSON Schema cannot state. Reduction is checked with the
  covering rule of section 9.5, written out below from the text;
- the conformance corpus in tests/: every case file validates against
  tests/case.schema.json, is listed in tests/index.json under its own
  id, level and kind, and no two cases share an id; the index's counts
  are the cases' counts; and every baseline a derive case expects is
  held to the rules above, as velaris.capabilities/1.

With --audits DIR, every *.json directly in DIR is validated as
velaris.audit/1 as well: the way to hold the schema against a
reference implementation's real output. With --capabilities FILE, that
baseline is held to the same rules as the examples - the way to hold
the schema against the baseline a real repository commits.

Needs the jsonschema package (pip install jsonschema).
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
# 0.11.0: the types are named at velaris-lang.dev; a Statement written by
# velaris-lang 4.2 to 8.2.1 names them at the earlier address, and is read as
# the same type (sections 8.5 and 8.7). The examples are those Statements.
PREDICATE_TYPE = "https://velaris-lang.dev/capability/v1"
RECEIPT_TYPE = "https://velaris-lang.dev/receipt/v1"
PREDICATE_TYPES = (PREDICATE_TYPE,
                   "https://gowrishankar-infra.github.io/velaris-lang/capability/v1")
RECEIPT_TYPES = (RECEIPT_TYPE,
                 "https://gowrishankar-infra.github.io/velaris-lang/receipt/v1")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def errors_of(validator, doc) -> list:
    return [f"{'/'.join(map(str, e.absolute_path)) or '(top)'}: {e.message}"
            for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))]


# ---- SPEC.md 9.5, for the reduction check --------------------------------

def norm(p: str) -> str:
    rooted = p.startswith("/")
    out = []
    for part in p.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if out and out[-1] != "..":
                out.pop()
                continue
            if rooted and not out:
                continue
        out.append(part)
    text = "/".join(out)
    return "/" + text if rooted else (text or ".")


# The effects a grant names on their own, with nothing after a colon.
# `declassify` joined them in 0.7; before that "declassify" fell
# through parts() to the net branch and read as a grant of every
# host, so a baseline holding it reported every net: grant as
# redundant. velaris-spec 3.1.
PLAIN = ("io", "env", "clock", "rand", "declassify")


def parts(g: str) -> tuple:
    if g in PLAIN:
        return (g,)
    kind, _, rest = g.partition(":")
    if kind in ("ffi", "tool"):            # tool: 0.13.0, one tool by name
        return (kind, rest or None)
    if kind == "fs":
        d, _, p = rest.partition(":")
        return ("fs", d or None, p or None)
    if not rest:
        return ("net", None, None)
    if rest.startswith("["):
        end = rest.index("]")
        host, tail = rest[1:end], rest[end + 1:]
        return ("net", host, int(tail[1:]) if tail else None)
    host, sep, port = rest.rpartition(":")
    if sep and port.isdigit():
        return ("net", host, int(port))
    return ("net", rest, None)


def host_matches(pattern: str, host: str) -> bool:
    if pattern.startswith("*."):
        tail = pattern[2:]
        return host.endswith("." + tail) and "." not in host[:-len(tail) - 1] \
            and len(host) > len(tail) + 1
    return pattern == host


def covers(b: tuple, c: tuple) -> bool:
    if b[0] != c[0]:
        return False
    if b[0] in PLAIN:
        return True
    if b[0] in ("ffi", "tool"):
        return b[1] is None or b[1] == c[1]
    if b[1] is None:
        return True
    if c[1] is None:
        return False
    if b[0] == "fs":
        if b[1] != c[1]:
            return False
        if b[2] is None:
            return True
        if c[2] is None:
            return False
        q, p = norm(b[2]), norm(c[2])
        if q == p:
            return True
        if "\\" in q or "\\" in p:
            return False
        if q == ".":
            return not (p.startswith("/") or p == ".." or p.startswith("../"))
        if q == "/":
            return p.startswith("/")
        return p.startswith(q + "/")
    (host, port), (want, want_port) = (b[1], b[2]), (c[1], c[2])
    if port is not None and port != want_port:
        return False
    if host.startswith("*.") and want.startswith("*."):
        return host == want
    if want.startswith("*."):
        return False
    return host_matches(host, want)


def grant_list_problems(grants: list, where: str) -> list:
    problems = []
    if grants != sorted(grants):
        problems.append(f"{where}: grants are not sorted")
    for g in grants:
        for h in grants:
            if g != h and covers(parts(h), parts(g)) and (
                    not covers(parts(g), parts(h)) or h < g):
                problems.append(f"{where}: {g!r} is covered by {h!r}, so "
                                f"the list is not reduced")
    return problems


def capabilities_problems(caps, doc) -> list:
    problems = errors_of(caps, doc)
    if problems:
        return problems
    files = [p["file"] for p in doc["programs"]]
    if files != sorted(files):
        problems.append("programs are not sorted by file")
    if len(files) != len(set(files)):
        problems.append("a file is listed twice")
    problems += grant_list_problems(doc["surface"]["grants"], "surface")
    for p in doc["programs"]:
        if p.get("compiles") is not False:
            problems += grant_list_problems(p["grants"], p["file"])
            for name, effects in p["functions"].items():
                if effects != sorted(effects):
                    problems.append(f"{p['file']}: {name}'s effects are not "
                                    f"sorted")
    return problems


def corpus_problems(caps) -> list:
    """What is wrong with tests/: see the module docstring."""
    tests = ROOT / "tests"
    schema = load(tests / "case.schema.json")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        return [f"tests/case.schema.json is not a valid schema: {e}"]
    cases = Draft202012Validator(schema)
    index = load(tests / "index.json")
    problems = []
    if index.get("format") != "velaris.conformance-corpus/1":
        problems.append("index.json: format is not "
                        "velaris.conformance-corpus/1")
    listed = {}
    for e in index.get("cases", []):
        if e["id"] in listed:
            problems.append(f"index.json lists {e['id']} twice")
        listed[e["id"]] = e
    on_disk = sorted(p for level in ("L1", "L2", "L3")
                     for p in (tests / level).glob("*.json"))
    seen, per_level = set(), {"1": 0, "2": 0, "3": 0}
    for path in on_disk:
        rel = path.relative_to(tests).as_posix()
        doc = load(path)
        errs = errors_of(cases, doc)
        if errs:
            problems.append(f"{rel}: {errs[0]}")
            continue
        entry = listed.get(doc["id"])
        if path.stem != doc["id"]:
            problems.append(f"{rel}: its id is {doc['id']}")
        if f"L{doc['level']}" != path.parent.name:
            problems.append(f"{rel}: level {doc['level']} in {path.parent.name}")
        if entry is None:
            problems.append(f"{rel} is not in index.json")
        elif (entry["file"], entry["level"], entry["kind"]) != (
                rel, doc["level"], doc["kind"]):
            problems.append(f"index.json disagrees with {rel}")
        if doc["id"].lower() in seen:
            problems.append(f"{rel}: another case has the id {doc['id']}")
        seen.add(doc["id"].lower())
        per_level[str(doc["level"])] += 1
        if doc["kind"] == "derive":
            body = dict(doc["expect"], schema="velaris.capabilities/1",
                        velaris_version="0", date="2026-01-01")
            problems += [f"{rel}: {p}" for p in capabilities_problems(caps, body)]
    problems += [f"index.json lists {i}, which has no file"
                 for i in sorted(set(listed) - {p.stem for p in on_disk})]
    for level, n in per_level.items():
        said = index.get("levels", {}).get(level, {}).get("cases")
        if said != n:
            problems.append(f"index.json says level {level} has {said} "
                            f"cases; there are {n}")
    return problems


def main(argv: list) -> int:
    failed = 0

    def report(label: str, problems: list) -> None:
        nonlocal failed
        if problems:
            failed += 1
            print(f"FAIL  {label}")
            for p in problems[:10]:
                print(f"      {p}")
        else:
            print(f"ok    {label}")

    schemas = {}
    for path in sorted((ROOT / "schemas").glob("*.json")):
        schema = load(path)
        try:
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = Draft202012Validator(schema)
            report(f"schemas/{path.name} is a valid draft 2020-12 schema", [])
        except Exception as e:  # SchemaError, with the reason
            report(f"schemas/{path.name} is a valid draft 2020-12 schema", [str(e)])

    audit = schemas.get("velaris.audit.1.schema.json")
    caps = schemas.get("velaris.capabilities.1.schema.json")
    if audit is None or caps is None:
        print("FAIL  the audit and capabilities/1 schemas must be present and valid")
        return 1

    for path in sorted((ROOT / "examples").rglob("*.audit.json")):
        report(f"{path.relative_to(ROOT).as_posix()} is velaris.audit/1",
               errors_of(audit, load(path)))

    for path in sorted((ROOT / "examples").glob("*.capabilities.json")):
        report(f"{path.relative_to(ROOT).as_posix()} is velaris.capabilities/1",
               capabilities_problems(caps, load(path)))

    predicate = schemas.get("capability-predicate.v1.schema.json")
    for path in sorted((ROOT / "examples").glob("*statement.json")):
        doc = load(path)
        problems = []
        if doc.get("_type") != "https://in-toto.io/Statement/v1":
            problems.append("_type is not https://in-toto.io/Statement/v1")
        if doc.get("predicateType") not in PREDICATE_TYPES:
            problems.append(f"predicateType is not {PREDICATE_TYPE}, or the "
                            f"earlier spelling of it")
        subjects = doc.get("subject") or []
        if not subjects or not all(
                isinstance(s.get("name"), str) and len(
                    (s.get("digest") or {}).get("sha256", "")) == 64
                for s in subjects):
            problems.append("every subject needs a name and a sha256 digest")
        if predicate is None:
            problems.append("schemas/capability-predicate.v1.schema.json "
                            "is missing")
        else:
            problems += errors_of(predicate, doc.get("predicate"))
            problems += [f"audit: {p}" for p in errors_of(
                audit, (doc.get("predicate") or {}).get("audit"))]
        report(f"{path.relative_to(ROOT).as_posix()} is an in-toto Statement "
               f"of the capability/v1 predicate", problems)

    receipt_schema = schemas.get("receipt-predicate.v1.schema.json")
    receipts = sorted((ROOT / "examples").glob("*receipt.json"))
    if not receipts:
        report("examples/ holds a receipt the reference wrote",
               ["no examples/*receipt.json"])
    for path in receipts:
        doc = load(path)
        problems = []
        if doc.get("_type") != "https://in-toto.io/Statement/v1":
            problems.append("_type is not https://in-toto.io/Statement/v1")
        if doc.get("predicateType") not in RECEIPT_TYPES:
            problems.append(f"predicateType is not {RECEIPT_TYPE}, or the "
                            f"earlier spelling of it")
        subjects = doc.get("subject") or []
        if not subjects or not all(
                isinstance(s.get("name"), str) and len(
                    (s.get("digest") or {}).get("sha256", "")) == 64
                for s in subjects):
            problems.append("every subject needs a name and a sha256 digest")
        if receipt_schema is None:
            problems.append("schemas/receipt-predicate.v1.schema.json is "
                            "missing")
        else:
            problems += errors_of(receipt_schema, doc.get("predicate"))
        report(f"{path.relative_to(ROOT).as_posix()} is an in-toto Statement "
               f"of the receipt/v1 predicate", problems)

    index = load(ROOT / "tests" / "index.json")
    report(f"tests/: {len(index.get('cases', []))} conformance cases, each "
           f"valid, listed and unique", corpus_problems(caps))

    if "--audits" in argv:
        where = Path(argv[argv.index("--audits") + 1])
        docs = sorted(where.glob("*.json"))
        bad = [(p.name, errs) for p in docs if (errs := errors_of(audit, load(p)))]
        report(f"{len(docs)} documents in {where} are velaris.audit/1",
               [f"{name}: {errs[0]}" for name, errs in bad])

    if "--capabilities" in argv:
        path = Path(argv[argv.index("--capabilities") + 1])
        report(f"{path} is velaris.capabilities/1",
               capabilities_problems(caps, load(path)))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
