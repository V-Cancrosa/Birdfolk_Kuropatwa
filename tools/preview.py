#!/usr/bin/env python3
"""Podgląd klucza: litera łacińska nad znakiem Kuropatwy, oba style + próbka tekstu."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kuropatwa.charset import REQUIRED  # noqa: E402

SAMPLE = [
    "kosen, !ogä!! kornik. kosen, kösal.",
    "na = !jack! durtan-in !thorlene!, sekorat.",
    "na kir-ło kate. sena na kir-ka-ło sete.",
]


def main(out: Path, scale: int = 1):
    big = 56 * scale
    fc = ImageFont.truetype(str(ROOT / "dist/kuropatwa.ttf"), big)
    fd = ImageFont.truetype(str(ROOT / "dist/kuropatwa-drap.ttf"), big)
    fl = ImageFont.truetype("DejaVuSans.ttf", 16 * scale)
    cols, cw, ch = 16, 78 * scale, 210 * scale
    rows = (len(REQUIRED) + cols - 1) // cols
    W = cols * cw + 40 * scale
    H = rows * ch + 3 * 90 * scale * 2 + 60 * scale
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(REQUIRED):
        x = 20 * scale + (i % cols) * cw
        y = 10 * scale + (i // cols) * ch
        d.text((x + 4 * scale, y), c, font=fl, fill=90)
        d.text((x, y + 20 * scale), c, font=fc, fill=0)
        d.text((x, y + 105 * scale), c, font=fd, fill=0)
    y = rows * ch + 20 * scale
    for f in (fc, fd):
        for line in SAMPLE:
            d.text((20 * scale, y), line, font=f, fill=0)
            y += 90 * scale
    im.save(out)
    print(out)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs/preview.png")
