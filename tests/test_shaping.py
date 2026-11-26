"""Kształtowanie tekstu (HarfBuzz): dwie role myślnika (spec v0.2, część A)."""
import pytest
import uharfbuzz as hb

from kuropatwa.build import build_font


@pytest.fixture(scope="module", params=["clean", "drap"])
def shaper(request, tmp_path_factory):
    p = tmp_path_factory.mktemp("s") / f"{request.param}.ttf"
    build_font(request.param).save(p)
    face = hb.Face(hb.Blob.from_file_path(str(p)))
    font = hb.Font(face)

    def names(text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf)
        return [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]
    return names


def _hyphens(glyphs):
    return [g for g in glyphs if g.startswith("uni002D") or g == "uni2013"]


def test_morpheme_hyphen_between_letters(shaper):
    assert _hyphens(shaper("na-ne-nir")) == ["uni002D.morph", "uni002D.morph"]
    assert _hyphens(shaper("kir-ka-ło")) == ["uni002D.morph", "uni002D.morph"]


def test_morpheme_hyphen_after_name_marker(shaper):
    assert _hyphens(shaper("!thorlene!-or")) == ["uni002D.morph"]


def test_uppercase_letters_count_as_word(shaper):
    assert _hyphens(shaper("NA-NE")) == ["uni002D.morph"]


def test_list_dash_at_line_start(shaper):
    assert _hyphens(shaper("- tekan")) == ["uni002D"]


def test_hyphen_between_digits_is_list_mark(shaper):
    assert _hyphens(shaper("3-5")) == ["uni002D"]


def test_en_dash_is_always_list_mark(shaper):
    assert shaper("na–ne")[2] == "uni2013"  # ten sam kształt co punkt wyliczenia, nigdy .morph


def test_native_fused_text_has_no_hyphen(shaper):
    assert _hyphens(shaper("nanenir")) == []
