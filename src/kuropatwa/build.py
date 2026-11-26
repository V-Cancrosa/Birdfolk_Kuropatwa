"""Składanie fontu Kuropatwa (TrueType) i zapis plików webowych."""
from __future__ import annotations

from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.roundingPen import RoundingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

from .glyphs import glyph_table
from .render import GRID, advance, render

VERSION = "0.1.0"
UPM = 1000
ASCENT, DESCENT = 1000, -200
FAMILIES = {"clean": "Kuropatwa", "drap": "Kuropatwa Drap"}
FILE_STEMS = {"clean": "kuropatwa", "drap": "kuropatwa-drap"}


def _glyph_name(ch: str) -> str:
    return f"uni{ord(ch):04X}"


def _draw(path) -> object:
    pen = TTGlyphPen(None)
    path.draw(RoundingPen(pen))
    return pen.glyph()


def build_font(style: str) -> TTFont:
    table = glyph_table()
    order = [".notdef", "space"] + [_glyph_name(c) for c in table]
    glyphs, metrics, cmap = {}, {}, {}

    notdef = TTGlyphPen(None)
    for x0, y0, x1, y1 in ((60, 0, 360, 700), (110, 50, 310, 650)):
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        if x0 != 60:
            pts.reverse()
        notdef.moveTo(pts[0])
        for p in pts[1:]:
            notdef.lineTo(p)
        notdef.closePath()
    glyphs[".notdef"] = notdef.glyph()
    metrics[".notdef"] = (420, 60)
    glyphs["space"] = TTGlyphPen(None).glyph()
    metrics["space"] = (round(22 * GRID), 0)
    cmap[0x20] = "space"
    cmap[0xA0] = "space"

    for ch, spec in table.items():
        name = _glyph_name(ch)
        g = _draw(render(spec, style))
        glyphs[name] = g
        xmin = getattr(g, "xMin", 0) if g.numberOfContours else 0
        metrics[name] = (advance(spec), xmin)
        cmap[ord(ch)] = name
        up = ch.upper()
        if len(up) == 1 and up != ch:  # brak wielkich liter: WIELKA → ten sam znak
            cmap[ord(up)] = name
    if "ß" in table:
        cmap[0x1E9E] = _glyph_name("ß")

    family = FAMILIES[style]
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    # lsb z faktycznych konturów
    glyf = fb.font["glyf"]
    hmtx = {}
    for n in order:
        g = glyf[n]
        g.recalcBounds(glyf)
        hmtx[n] = (metrics[n][0], g.xMin if g.numberOfContours else 0)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT)
    fb.setupNameTable({
        "familyName": family,
        "styleName": "Regular",
        "uniqueFontIdentifier": f"{family.replace(' ', '')}-{VERSION}",
        "fullName": family,
        "psName": family.replace(" ", "") + "-Regular",
        "version": f"Version {VERSION}",
        "designer": "V. Cancrosa & Claude",
        "description": "Kuropatwa — pismo Birdfolk (Wspólny Zwierzoludzki), Whitewood.",
    })
    fb.setupOS2(sTypoAscender=ASCENT, sTypoDescender=DESCENT, sTypoLineGap=120,
                usWinAscent=ASCENT, usWinDescent=-DESCENT, sxHeight=700, sCapHeight=700,
                fsType=0, achVendID="VCAN")
    fb.setupPost()
    fb.setupHead(unitsPerEm=UPM, fontRevision=float(VERSION.rsplit(".", 1)[0]))
    return fb.font


CSS_TEMPLATE = """/* Kuropatwa — pismo Birdfolk. Wygenerowane przez tools/build.py */
@font-face {{
  font-family: "Kuropatwa";
  src: url("kuropatwa.woff2") format("woff2"), url("kuropatwa.woff") format("woff");
  font-display: swap;
}}
@font-face {{
  font-family: "Kuropatwa Drap";
  src: url("kuropatwa-drap.woff2") format("woff2"), url("kuropatwa-drap.woff") format("woff");
  font-display: swap;
}}
/* Użycie: <span class="kuropatwa">kosen, !ogä!! kornik.</span> */
.kuropatwa {{ font-family: "Kuropatwa", serif; font-variant-ligatures: normal; }}
.kuropatwa-drap {{ font-family: "Kuropatwa Drap", "Kuropatwa", serif; }}
"""


def write_all(out_dir: Path) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for style, stem in FILE_STEMS.items():
        font = build_font(style)
        for flavor, ext in ((None, "ttf"), ("woff", "woff"), ("woff2", "woff2")):
            font.flavor = flavor
            p = out_dir / f"{stem}.{ext}"
            font.save(p)
            written.append(p)
    css = out_dir / "kuropatwa.css"
    css.write_text(CSS_TEMPLATE.format(), encoding="utf-8")
    written.append(css)
    return written
