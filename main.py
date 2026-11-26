#!/usr/bin/env python3
"""Entry program: copy the front-page image to /output/entry.png.

Standard library only. Deterministic: the same bytes every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = HERE / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG")
    if len(data) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT)
    print(f"wrote {OUT} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
