#!/usr/bin/env python3
"""Check the schemas, and the examples against them.

usage: python tools/validate.py [--audits DIR] [--capabilities FILE]

- every file in schemas/ must be a valid JSON Schema (draft 2020-12);
- every examples/**/*.audit.json must validate as velaris.audit/1;
- every examples/*.capabilities.json must validate as
  velaris.capabilities/1, with its programs sorted by file and unique,
  and every grant list sorted and reduced - rules of SPEC.md section
  9.2 that JSON Schema cannot state. Reduction is checked with the
  covering rule of section 9.5, written out below from the text.

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


def parts(g: str) -> tuple:
    if g in ("io", "env", "clock", "rand"):
        return (g,)
    kind, _, rest = g.partition(":")
    if kind == "ffi":
        return ("ffi", rest or None)
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
    if b[0] in ("io", "env", "clock", "rand"):
        return True
    if b[0] == "ffi":
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
