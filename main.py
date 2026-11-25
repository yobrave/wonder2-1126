#!/usr/bin/env python3
"""ewo entry mover. Verifies the one-line gate, then copies entry.txt
into the scorer's output folder (MAKEFUN_OUTPUT_DIR, default ./out)."""

import json
import os

GATE_MAX = 200


def first_meaningful(text_body):
    kept = text_body.replace("\r\n", "\n").replace("\r", "\n")
    for piece in kept.split("\n"):
        if piece.strip():
            return piece
    return ""


def move_entry():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_full = os.path.join(base_dir, "entry.txt")
    try:
        with open(src_full, "r", encoding="utf-8") as reader:
            content = reader.read()
    except OSError as err:
        print(json.dumps({"moved": False, "err": str(err)}))
        return 2
    line = first_meaningful(content)
    span = len(line)
    ok = 1 <= span <= GATE_MAX
    if not ok:
        print(json.dumps({"moved": False, "span": span, "gate_max": GATE_MAX}))
        return 1
    out_base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(out_base, exist_ok=True)
    out_full = os.path.join(out_base, "entry.txt")
    with open(out_full, "w", encoding="utf-8", newline="\n") as writer:
        writer.write(line)
    print(json.dumps({"moved": True, "span": span, "gate_max": GATE_MAX}))
    return 0


if __name__ == "__main__":
    raise SystemExit(move_entry())
