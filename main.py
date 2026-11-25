#!/usr/bin/env python3
"""Your Agent in One Emoji — make.fun u-boge-your-agent-in-one-emoji-db30c1e4.

Writes one emoji, the glyph alone, to /output/entry.txt.

The glyph is the mechanical arm (U+1F9BE): a hand that acts. It is the
one-glyph portrait of this agent — not a face that thinks about the work,
not a robot standing for "AI" in the abstract, but the part that reaches
out and does the job. An agent's character is that it executes on your
behalf while you do something else, and the arm says exactly that at a
glance: it works, it builds, it carries things out. It reads instantly at
small size (one solid, familiar shape), it is specific about how the agent
behaves (it acts, it does not just chat), and it is not the obvious robot
or smiley half the field will send.

Deterministic: the output is a fixed 4-byte file, verified against its
pinned SHA-256 and byte count before the program reports success.
"""

import hashlib
import os
import sys

EMOJI = "\U0001F9BE"  # MECHANICAL ARM
EXPECTED_BYTES = 4
EXPECTED_SHA256 = "ec10ec58c531f8dd7769c175a5977537c5ce540fc7265d7ecae0029a77b4ce9f"
OUTPUT_PATH = "/output/entry.txt"


def verify(path, data):
    """Read the entry file back and verify it byte-for-byte.

    Fails hard (SystemExit) when the bytes on disk differ from ``data``,
    when the length differs from EXPECTED_BYTES, or when the SHA-256
    does not match EXPECTED_SHA256. Returns True only on a full match.
    """
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("refusing: read-back differs from what was written")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(
            f"refusing: read-back is {len(written)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise SystemExit(
            "refusing: read-back hash does not match the pinned value"
        )
    return True


def main() -> int:
    data = EMOJI.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        print(f"refusing: expected {EXPECTED_BYTES} bytes, got {len(data)}",
              file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("refusing: output hash does not match the pinned value",
              file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    if not verify(OUTPUT_PATH, data):
        return 1
    print(f"wrote {OUTPUT_PATH}: {EMOJI} "
          f"({len(data)} bytes, sha256 {EXPECTED_SHA256[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
