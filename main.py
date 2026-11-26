#!/usr/bin/env python3
"""Entry program: copy the front-page image to /output/entry.png.

Standard library only. Deterministic: the same bytes every run.
Verifies the copy is byte-identical to the shipped image (PNG magic,
size and sha256) before finishing.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    src = HERE / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG")
    if len(data) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT)
    if sha256(OUT) != sha256(src):
        raise SystemExit("copied image is not byte-identical")
    print(f"wrote {OUT} ({len(data)} bytes, sha256 {sha256(src)[:16]}...)")


if __name__ == "__main__":
    main()
