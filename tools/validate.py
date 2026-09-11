#!/usr/bin/env python3
"""Check the schemas, and the examples against them.

usage: python tools/validate.py [--audits DIR]

- every file in schemas/ must be a valid JSON Schema (draft 2020-12);
- every examples/**/*.audit.json must validate as velaris.audit/1;
- every examples/*.capabilities.json must validate as
  velaris.capabilities/0, with its programs sorted by file and each
  entry's grants sorted - two rules of SPEC.md section 9.2 that JSON
  Schema cannot state. (Reduction, the other rule it cannot state, is
  not checked here.)

With --audits DIR, every *.json directly in DIR is validated as
velaris.audit/1 as well: the way to hold the schema against a
reference implementation's real output.

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
    caps = schemas.get("velaris.capabilities.0.schema.json")
    if audit is None or caps is None:
        print("FAIL  both schemas must be present and valid")
        return 1

    for path in sorted((ROOT / "examples").rglob("*.audit.json")):
        report(f"{path.relative_to(ROOT).as_posix()} is velaris.audit/1",
               errors_of(audit, load(path)))

    for path in sorted((ROOT / "examples").glob("*.capabilities.json")):
        doc = load(path)
        problems = errors_of(caps, doc)
        if not problems:
            files = [p["file"] for p in doc["programs"]]
            if files != sorted(files):
                problems.append("programs are not sorted by file")
            for p in doc["programs"]:
                if p["grants"] != sorted(p["grants"]):
                    problems.append(f"{p['file']}: grants are not sorted")
        report(f"{path.relative_to(ROOT).as_posix()} is velaris.capabilities/0", problems)

    if "--audits" in argv:
        where = Path(argv[argv.index("--audits") + 1])
        docs = sorted(where.glob("*.json"))
        bad = [(p.name, errs) for p in docs if (errs := errors_of(audit, load(p)))]
        report(f"{len(docs)} documents in {where} are velaris.audit/1",
               [f"{name}: {errs[0]}" for name, errs in bad])

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
