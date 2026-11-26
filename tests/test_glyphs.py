from kuropatwa.charset import REQUIRED, LAYERS
from kuropatwa.glyphs import glyph_table


def test_all_required_chars_present():
    table = glyph_table()
    missing = [c for c in REQUIRED if c not in table]
    assert missing == []


def test_layers_valid():
    for ch, g in glyph_table().items():
        assert g.layer in LAYERS, ch


def test_core_has_no_arcs_and_mammal_has_exactly_one():
    for ch, g in glyph_table().items():
        arcs = sum(1 for s in g.strokes if s.arc)
        if g.layer == "core":
            assert arcs == 0, ch
        if g.layer == "mammal":
            assert arcs == 1, ch


def test_labials_extend_their_partner():
    t = glyph_table()
    for lab, partner in {"m": "n", "p": "t", "b": "d", "f": "h", "w": "ł"}.items():
        partner_pts = [s.pts for s in t[partner].strokes]
        lab_pts = [s.pts for s in t[lab].strokes if not s.arc]
        assert lab_pts == partner_pts, lab


def test_umlaut_is_bar_not_dots():
    t = glyph_table()
    for ch in "äöü":
        assert any(s.kind == "bar" for s in t[ch].strokes), ch


def test_no_two_glyphs_identical():
    seen = {}
    for ch, g in glyph_table().items():
        key = (g.branch, tuple(tuple(s.pts) for s in g.strokes))
        assert key not in seen, f"{ch} == {seen.get(key)}"
        seen[key] = ch
