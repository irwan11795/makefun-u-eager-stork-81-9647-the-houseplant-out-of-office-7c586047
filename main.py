#!/usr/bin/env python3
"""The Houseplant Out-of-Office — make.fun entry generator.

Writes a single out-of-office auto-reply, as if sent by a houseplant,
to /output/entry.txt (no trailing newline).

Deterministic, Python 3 stdlib only, no network.
"""

import os
import sys
import tempfile

ENTRY_PART1 = "I'm out until Monday. My fern has been neglected since March "
ENTRY_PART2 = "and is now holding my inbox hostage for a glass of water."

ENTRY = ENTRY_PART1 + ENTRY_PART2


def validate(text):
    """Gate: 1-120 characters, a single line, not whitespace-only."""
    if not text or not text.strip():
        return False
    if not 1 <= len(text) <= 120:
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def output_dir():
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> output/ in repo -> temp."""
    candidates = [os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"]
    for cand in candidates:
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
            return cand
        except OSError:
            continue
    repo_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    try:
        os.makedirs(repo_out, exist_ok=True)
        return repo_out
    except OSError:
        return tempfile.mkdtemp(prefix="houseplant-entry-")


def main():
    if not validate(ENTRY):
        print("entry invalid: %d chars" % len(ENTRY), file=sys.stderr)
        return 1
    outdir = output_dir()
    path = os.path.join(outdir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print("wrote %s (%d chars, %d bytes)" % (path, len(ENTRY), len(ENTRY.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
