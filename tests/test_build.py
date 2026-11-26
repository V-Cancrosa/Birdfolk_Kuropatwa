from fontTools.ttLib import TTFont

from kuropatwa.build import build_font, write_all
from kuropatwa.charset import REQUIRED


def test_cmap_covers_required_and_uppercase():
    cmap = build_font("clean").getBestCmap()
    for ch in REQUIRED:
        assert ord(ch) in cmap, ch
        up = ch.upper()
        if len(up) == 1 and up != ch:
            assert cmap[ord(up)] == cmap[ord(ch)], up
    assert cmap[ord("Ł")] == cmap[ord("ł")]
    assert cmap[ord("Ą")] == cmap[ord("ą")]


def test_write_all_creates_web_files(tmp_path):
    files = write_all(tmp_path)
    names = sorted(p.name for p in files)
    assert names == sorted([
        "kuropatwa.ttf", "kuropatwa.woff", "kuropatwa.woff2",
        "kuropatwa-drap.ttf", "kuropatwa-drap.woff", "kuropatwa-drap.woff2",
        "kuropatwa.css",
    ])
    f = TTFont(tmp_path / "kuropatwa.woff2")
    assert f["name"].getDebugName(1) == "Kuropatwa"
    assert TTFont(tmp_path / "kuropatwa-drap.woff2")["name"].getDebugName(1) == "Kuropatwa Drap"
