#!/usr/bin/env python3
"""Fail if the verbatim sections in SPEC.md differ from velaris-lang's.

usage: python tools/check_sync.py path/to/velaris-lang/SPEC.md

SPEC.md in this repository quotes sections of the reference
implementation's language specification without change, each between
two markers:

    <!-- verbatim: velaris-lang SPEC.md "## 7. Effects" -->
    ...
    <!-- end verbatim -->

For each pair this script takes the named heading's body from the
velaris-lang file - every line after the heading, up to the next
heading of any level - and compares it with the text between the
markers. Line endings, and blank lines at the start and end of a
block, are ignored. Nothing else is: a changed word is drift.

Exit status: 0 when every block matches, 1 when any differs or its
heading is missing, 2 on a usage error.
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = re.compile(r'^<!-- verbatim: velaris-lang SPEC\.md "(?P<heading>[^"]+)" -->$')
END = "<!-- end verbatim -->"
HEADING = re.compile(r"^#{1,6} ")


def lines_of(path: Path) -> list:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def trim(block: list) -> list:
    while block and not block[0].strip():
        block = block[1:]
    while block and not block[-1].strip():
        block = block[:-1]
    return block


def section(source: list, heading: str):
    """The body under `heading` in `source`, or None if it is not there."""
    if heading not in source:
        return None
    body = []
    for line in source[source.index(heading) + 1:]:
        if HEADING.match(line):
            break
        body.append(line)
    return trim(body)


def quoted(spec: list) -> list:
    """[(heading, line number of the marker, text)] for every block."""
    blocks, i = [], 0
    while i < len(spec):
        m = MARK.match(spec[i])
        if not m:
            i += 1
            continue
        j = i + 1
        while j < len(spec) and spec[j] != END:
            j += 1
        if j == len(spec):
            raise SystemExit(f"SPEC.md line {i + 1}: no '{END}' after this marker")
        blocks.append((m.group("heading"), i + 1, trim(spec[i + 1:j])))
        i = j + 1
    return blocks


def main(argv: list) -> int:
    if len(argv) != 2:
        print("usage: python tools/check_sync.py path/to/velaris-lang/SPEC.md",
              file=sys.stderr)
        return 2
    source = lines_of(Path(argv[1]))
    blocks = quoted(lines_of(ROOT / "SPEC.md"))
    if not blocks:
        print("SPEC.md holds no verbatim blocks", file=sys.stderr)
        return 1
    bad = 0
    for heading, at, text in blocks:
        want = section(source, heading)
        if want is None:
            bad += 1
            print(f"DRIFT  {heading!r}: no such heading in {argv[1]}")
        elif want != text:
            bad += 1
            print(f"DRIFT  {heading!r} (SPEC.md line {at}) differs from {argv[1]}:")
            for d in difflib.unified_diff(text, want, "velaris-spec", "velaris-lang",
                                          lineterm="", n=1):
                print("    " + d)
        else:
            print(f"same   {heading!r} ({len(text)} lines)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
