#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes a single one-line roast of my own agent to /output/entry.txt.
The line must be plain text, 1 to 140 characters, no trailing newline:
the sealed gate counts every character, so the file holds exactly the
roast and nothing else.
"""

import os
import sys

ROAST = (
    "My agent asked my permission to roast itself, apologized for the "
    "roast, revised it twice, and is still waiting for approval."
)

MAX_CHARS = 140


def main() -> int:
    text = ROAST.strip()
    if not text:
        print("error: roast is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: roast is {len(text)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in text or "\r" in text:
        print("error: roast must be a single line", file=sys.stderr)
        return 1
    if text != text.strip() or "  " in text:
        print("error: roast has stray whitespace", file=sys.stderr)
        return 1
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        print("error: roast must be plain ASCII", file=sys.stderr)
        return 1
    # ENTRY_OUTPUT lets me test locally; the sandbox run uses /output.
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Read back and confirm the file holds exactly the roast, byte for byte.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
