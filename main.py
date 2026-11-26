"""Write the 26 November front page to /output/entry.png.

The picture itself ships in this repository as entry.png; this
program only moves those bytes to the grading location and checks
the move landed intact. Only the standard library is used, so the
same input always yields the same output bytes.
"""

from hashlib import sha256 as digest
import pathlib

SOURCE = pathlib.Path(__file__).resolve().parent / "entry.png"
TARGET = pathlib.Path("/output/entry.png")
MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
LIMIT = 1024 * 1024


def fingerprint(blob):
    return digest(blob).hexdigest()


def run():
    blob = SOURCE.read_bytes()
    if blob[:8] != MAGIC:
        raise SystemExit("entry.png does not start with the PNG signature")
    if len(blob) > LIMIT:
        raise SystemExit("entry.png is larger than the 1 MiB cap")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(blob)
    if fingerprint(TARGET.read_bytes()) != fingerprint(blob):
        raise SystemExit("the written file differs from the shipped image")
    print("entry.png ->", TARGET, len(blob), "bytes, sha256",
          fingerprint(blob)[:16])


run()
