from kuropatwa.glyphs import glyph_table
from kuropatwa.render import render


def _contours(path):
    return [tuple(c) for c in path.contours]


def test_render_both_styles_within_bounds():
    g = glyph_table()["a"]
    for style in ("clean", "drap"):
        p = render(g, style)
        xmin, ymin, xmax, ymax = p.bounds
        assert xmax > xmin and ymax > ymin
        assert ymin >= -200 and ymax <= 1000


def test_all_glyphs_within_vertical_limits():
    for ch, g in glyph_table().items():
        for style in ("clean", "drap"):
            _, ymin, _, ymax = render(g, style).bounds
            assert -200 <= ymin and ymax <= 1000, (ch, style, ymin, ymax)


def test_drap_deterministic_and_seeded():
    g = glyph_table()["k"]
    assert _contours(render(g, "drap", 1)) == _contours(render(g, "drap", 1))
    assert _contours(render(g, "drap", 1)) != _contours(render(g, "drap", 2))
