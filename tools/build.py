#!/usr/bin/env python3
"""Buduje fonty Kuropatwa do dist/ (i wzornik, jeśli dostępny)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kuropatwa.build import write_all  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
import specimen  # noqa: E402

if __name__ == "__main__":
    for p in write_all(ROOT / "dist"):
        print(p.relative_to(ROOT))
    print(specimen.build(ROOT / "specimen/index.html", "../dist/").relative_to(ROOT))
