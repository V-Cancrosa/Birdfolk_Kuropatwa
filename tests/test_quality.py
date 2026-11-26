"""Kontrola jakości: rozróżnialność w 16 px i deterministyczność."""
from itertools import combinations

import pytest
from PIL import Image, ImageDraw, ImageFont

from kuropatwa.build import build_font
from kuropatwa.charset import REQUIRED
from kuropatwa.glyphs import glyph_table

SIZE = 16
# Minimalna liczba wyraźnie różnych pikseli (kontrast >96/255) między dwoma znakami.
# 16 px: ciało znaku ma ~11 px, cecha odróżniająca (podeszwa d, przekreślenie ł, nacięcie
# cyfry) to 3–5 wyraźnych pikseli — sprawdzone wzrokowo na powiększeniu (docs/KAMIENIE.md).
MIN_DIFF_16 = 3
MIN_DIFF_24 = 6

# pary, które celowo są bliskie (ten sam znak bazowy z małym dopiskiem) — puste z założenia
ALLOWED_SIMILAR: set[frozenset[str]] = set()


@pytest.fixture(scope="module")
def font_file(tmp_path_factory):
    p = tmp_path_factory.mktemp("f") / "k.ttf"
    build_font("clean").save(p)
    return p


def _bitmap(font, ch, size=SIZE):
    im = Image.new("L", (size * 3, size * 2), 0)
    ImageDraw.Draw(im).text((2, 0), ch, font=font, fill=255)
    return im


def _diff(a, b):
    """Liczba pikseli różniących się wyraźnie (z wygładzaniem, jak widzi oko)."""
    return sum(1 for p, q in zip(a.getdata(), b.getdata()) if abs(p - q) > 96)


def _base_key(ch):
    """Szkielet bez dopisków nad gałęzią i pod linią — znaki o tym samym kluczu różnią się tylko dopiskiem."""
    g = TABLE[ch]
    return tuple(s.pts for s in g.strokes if min(y for _, y in s.pts) < 100 and min(y for _, y in s.pts) >= 0)


TABLE = glyph_table()


def _pairs(marked: bool):
    for a, b in combinations(REQUIRED, 2):
        if frozenset((a, b)) in ALLOWED_SIMILAR:
            continue
        same_base = _base_key(a) == _base_key(b)
        if same_base == marked:
            yield a, b


def _collisions(font_file, size, pairs, min_diff):
    font = ImageFont.truetype(str(font_file), size)
    maps = {c: _bitmap(font, c, size) for c in REQUIRED}
    return [(a, b, d) for a, b in pairs if (d := _diff(maps[a], maps[b])) < min_diff]


def test_different_bases_distinguishable_at_16px(font_file):
    assert _collisions(font_file, 16, _pairs(marked=False), MIN_DIFF_16) == []


def test_marked_variants_distinguishable_at_24px(font_file):
    """á/à, z/ż, o/ö itd. — dopiski nad gałęzią muszą się rozróżniać od 24 px."""
    assert _collisions(font_file, 24, _pairs(marked=True), MIN_DIFF_24) == []


def test_drap_build_is_deterministic():
    a = build_font("drap")["glyf"]
    b = build_font("drap")["glyf"]
    for name in a.keys():
        assert a[name].getCoordinates(a)[0] == b[name].getCoordinates(b)[0], name
