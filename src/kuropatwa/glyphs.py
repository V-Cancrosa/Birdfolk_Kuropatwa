"""Szkielety znaków Kuropatwy.

Siatka: 1 jednostka = 7 font units. y=0 to linia bazowa, y=100 to gałąź
(linia łącząca słowo). Litery wiszą pod gałęzią: spółgłoski do linii bazowej,
samogłoski do połowy (y=50). Znaki nad gałęzią (y>100) to diakrytyki
i gramatyczne ! ?.

Warstwy pochodzenia (historia pisma):
  core      rdzeń Corvum: proste rysy dziobem, bez łuków
  mammal    dopisek ssaków: partner bezwargowy + łuk „warg”
            (m→n, p→t, b→d, f→h, w→ł, tablica konwersji z dokumentu języka)
  nasal     ą ę: samogłoska + ogon pod linię
  loxodon   ä ö ü: samogłoska + ciężka belka nad gałęzią
  imperial  q v x y ß i akcenty romańskie: znak + haczyk obcości
  punct     interpunkcja i znaki gramatyczne
  digit     cyfry: pień + nacięcia (bez gałęzi, liczby stoją osobno)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

Pt = tuple[float, float]


@dataclass(frozen=True)
class Stroke:
    pts: tuple[Pt, ...]
    kind: str = "hang"   # hang: od gałęzi, ostry koniec | free: ostre końce | bar: płaska belka
    arc: bool = False


@dataclass(frozen=True)
class GlyphSpec:
    name: str
    layer: str
    width: float              # szerokość pola rysunku w siatce (bez marginesów)
    strokes: tuple[Stroke, ...]
    branch: bool = True       # czy znak niesie odcinek gałęzi


def S(*pts: Pt, kind: str = "hang") -> Stroke:
    return Stroke(tuple((float(x), float(y)) for x, y in pts), kind)


def arc(cx: float, cy: float, r: float, a0: float, a1: float, step: float = 10.0) -> Stroke:
    n = max(2, int(abs(a1 - a0) / step) + 1)
    pts = tuple(
        (round(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))), 3),
         round(cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))), 3))
        for i in range(n)
    )
    return Stroke(pts, "free", True)


# ---------------------------------------------------------------- rdzeń Corvum
# (szerokość, kreski)
CORE_CONSONANTS: dict[str, tuple[float, list[Stroke]]] = {
    "t": (24, [S((12, 100), (12, 0))]),
    "k": (44, [S((0, 100), (44, 0))]),
    "s": (40, [S((4, 100), (38, 64), (4, 34), (38, 0))]),
    "h": (40, [S((6, 100), (6, 0)), S((34, 100), (34, 0))]),
    "n": (46, [S((23, 100), (23, 42)), S((23, 42), (0, 0), kind="free"), S((23, 42), (46, 0), kind="free")]),
    "l": (40, [S((8, 100), (8, 52), (40, 14))]),
    "r": (42, [S((8, 100), (8, 0)), S((42, 100), (8, 48))]),
    "c": (46, [S((46, 100), (14, 0), (0, 36))]),
    "j": (38, [S((30, 100), (30, 44), (2, 0))]),
}

# dźwięczność: krótka „stopka” na końcu ostatniej rysy (t→d, k→g, s→z)
VOICED = {"d": "t", "g": "k", "z": "s"}

CORE_VOWELS: dict[str, tuple[float, list[Stroke]]] = {
    "e": (20, [S((10, 100), (10, 44))]),
    "a": (40, [S((0, 100), (20, 40), (40, 100))]),
    "i": (32, [S((4, 100), (4, 48)), S((28, 100), (28, 48))]),
    "o": (36, [S((18, 100), (0, 70), (18, 40), (36, 70), (18, 100), kind="free")]),
    "u": (38, [S((4, 100), (4, 42), (36, 42), (36, 74))]),
}


def _end(st: Stroke) -> Pt:
    return st.pts[-1]


def voiced(base: GlyphSpec) -> tuple[float, list[Stroke]]:
    """Podeszwa dźwięczności: pozioma rysa w prawo od końca ostatniej kreski."""
    x, y = _end(base.strokes[-1])
    foot = S((x - 4, y + 2), (x + 28, y + 2), kind="mark")
    return max(base.width, x + 26), list(base.strokes) + [foot]


# ------------------------------------------------------------ znaki nad gałęzią
def mark(kind: str, w: float) -> list[Stroke]:
    c = w / 2
    M = "mark"
    if kind == "soft":      # zmiękczenie (ć ń ś ź): pionowa rysa nad gałęzią
        return [S((c, 110), (c, 132), kind=M)]
    if kind == "dot":       # ż: krótka pozioma rysa
        return [S((c - 12, 118), (c + 12, 118), kind=M)]
    if kind == "bar":       # belka Loxodon (ä ö ü)
        return [S((c - 18, 118), (c + 18, 118), kind="bar")]
    if kind == "acute":
        return [S((c - 10, 109), (c + 10, 131), kind=M)]
    if kind == "grave":
        return [S((c + 10, 109), (c - 10, 131), kind=M)]
    if kind == "circ":
        return [S((c - 14, 108), (c, 128), (c + 14, 108), kind=M)]
    if kind == "tilde":
        return [S((c - 16, 110), (c - 6, 126), (c + 6, 112), (c + 16, 128), kind=M)]
    if kind == "hook":      # haczyk obcości (warstwa imperialna): flaga nad lewym końcem
        return [S((0, 100), (0, 124), (16, 130), kind=M)]
    raise ValueError(kind)


def nasal_tail(base: GlyphSpec) -> Stroke:
    """Ogon nosowy: od dołu samogłoski skośnie pod linię bazową."""
    bottom = min((p for s in base.strokes for p in s.pts), key=lambda p: p[1])
    return S(bottom, (bottom[0] + 14, -19), kind="mark")


def cedilla(base: GlyphSpec) -> Stroke:
    bottom = min((p for s in base.strokes for p in s.pts), key=lambda p: p[1])
    return S(bottom, (bottom[0] + 4, -12), (bottom[0] - 12, -19), kind="mark")


def lips(base: GlyphSpec) -> tuple[float, Stroke]:
    """Łuk „warg” po prawej stronie znaku — dopisek ssaków."""
    x = base.width + 6
    return x + 18, arc(x, 40, 18, -90, 90)


def with_marks(g: GlyphSpec, *kinds: str, layer: str | None = None) -> GlyphSpec:
    strokes = list(g.strokes)
    for k in kinds:
        strokes += mark(k, g.width)
    return replace(g, strokes=tuple(strokes), layer=layer or g.layer)


# ----------------------------------------------------------------- cyfry
def digit(n: int) -> GlyphSpec:
    stem_x = 10
    if n == 0:  # nol, „pustka”: pusty romb
        return GlyphSpec("zero", "digit", 40,
                         (S((20, 74), (2, 37), (20, 0), (38, 37), (20, 74), kind="free"),), branch=False)
    strokes = [S((stem_x, 100), (stem_x, 0))]
    notches = n
    if n >= 5:  # lin = „ciąć”: długie skośne cięcie przez dół pnia
        strokes.append(S((-8, 0), (36, 38), kind="mark"))
        notches = n - 5
    for i in range(notches):
        y = 100 - i * 18
        strokes.append(S((stem_x, y), (stem_x + 30, y - 12), kind="mark"))
    return GlyphSpec(f"d{n}", "digit", 40, tuple(strokes), branch=False)


# ----------------------------------------------------------------- budowa tabeli
def glyph_table() -> dict[str, GlyphSpec]:
    t: dict[str, GlyphSpec] = {}

    for ch, (w, st) in CORE_CONSONANTS.items():
        t[ch] = GlyphSpec(ch, "core", w, tuple(st))
    for ch, (w, st) in CORE_VOWELS.items():
        t[ch] = GlyphSpec(ch, "core", w, tuple(st))
    for ch, base in VOICED.items():
        w, st = voiced(t[base])
        t[ch] = GlyphSpec(ch, "core", w, tuple(st))

    # ł: l z przekreśleniem (rdzenne, niewargowe)
    t["ł"] = GlyphSpec("ł", "core", 40, t["l"].strokes + (S((-8, 54), (30, 86), kind="mark"),))

    # zmiękczenia i ż (rdzeń)
    for ch, base in {"ć": "c", "ń": "n", "ś": "s", "ź": "z"}.items():
        t[ch] = with_marks(replace(t[base], name=ch), "soft")
    t["ż"] = with_marks(replace(t["z"], name="ż"), "dot")

    # dopisek ssaków: partner + łuk
    for lab, partner in {"m": "n", "p": "t", "b": "d", "f": "h", "w": "ł"}.items():
        w, lip = lips(t[partner])
        t[lab] = GlyphSpec(lab, "mammal", w, t[partner].strokes + (lip,))

    # nosowe
    for ch, base in {"ą": "a", "ę": "e"}.items():
        t[ch] = GlyphSpec(ch, "nasal", t[base].width + 10, t[base].strokes + (nasal_tail(t[base]),))

    # Loxodon
    for ch, base in {"ä": "a", "ö": "o", "ü": "u"}.items():
        t[ch] = with_marks(replace(t[base], name=ch), "bar", layer="loxodon")

    # imperialne litery
    t["q"] = with_marks(replace(t["k"], name="q"), "hook", layer="imperial")
    t["v"] = with_marks(replace(t["w"], name="v"), "hook", layer="imperial")
    # x = imperialne „ks”: zrost k + s
    ks = (S((0, 100), (30, 0)), S((34, 100), (60, 66), (34, 36), (60, 4)))
    t["x"] = with_marks(GlyphSpec("x", "imperial", 60, ks), "hook")
    t["y"] = with_marks(GlyphSpec("y", "imperial", 30, (S((4, 100), (26, 48)),)), "hook")
    ss = (S((4, 100), (30, 64), (4, 34), (30, 0)), S((34, 100), (60, 64), (34, 34), (60, 0)))
    t["ß"] = with_marks(GlyphSpec("ß", "imperial", 60, ss), "hook")

    # akcenty romańskie (imperialne)
    accents = {
        "á": ("a", "acute"), "é": ("e", "acute"), "í": ("i", "acute"), "ó": ("o", "acute"), "ú": ("u", "acute"),
        "à": ("a", "grave"), "è": ("e", "grave"), "ì": ("i", "grave"), "ò": ("o", "grave"), "ù": ("u", "grave"),
        "â": ("a", "circ"), "ê": ("e", "circ"), "î": ("i", "circ"), "ô": ("o", "circ"), "û": ("u", "circ"),
        "ñ": ("n", "tilde"), "ã": ("a", "tilde"),
    }
    for ch, (base, k) in accents.items():
        t[ch] = with_marks(replace(t[base], name=ch), k, layer="imperial")
    t["ç"] = GlyphSpec("ç", "imperial", t["c"].width, t["c"].strokes + (cedilla(t["c"]),))

    # cyfry
    for n in range(10):
        t[str(n)] = digit(n)

    # interpunkcja i znaki gramatyczne
    P = "punct"
    dot = lambda y: S((10, y + 20), (0, y + 10), (10, y), (20, y + 10), (10, y + 20), kind="mark")  # noqa: E731
    t["."] = GlyphSpec("period", P, 20, (dot(0),), branch=False)
    t[","] = GlyphSpec("comma", P, 16, (S((14, 22), (0, -20)),), branch=False)
    t[":"] = GlyphSpec("colon", P, 20, (dot(0), dot(58)), branch=False)
    t[";"] = GlyphSpec("semicolon", P, 20, (S((16, 22), (2, -20)), dot(58)), branch=False)
    # ! i ? przebijają gałąź w górę — marker istotności / niepewności, część słowa
    t["!"] = GlyphSpec("exclam", P, 12, (S((6, 136), (6, 56), kind="free"),))
    t["?"] = GlyphSpec("question", P, 30, (S((6, 56), (6, 116), (28, 138), kind="mark"),))
    t["-"] = GlyphSpec("hyphen", P, 16, ())  # granica morfemów: goła gałąź
    t["="] = GlyphSpec("equal", P, 36, (S((0, 62), (36, 62), kind="bar"), S((0, 38), (36, 38), kind="bar")), branch=False)
    t["/"] = GlyphSpec("slash", P, 40, (S((0, -14), (40, 118), kind="mark"),), branch=False)
    t["+"] = GlyphSpec("plus", P, 36, (S((18, 68), (18, 12), kind="free"), S((-4, 40), (40, 40), kind="free")), branch=False)
    t["$"] = GlyphSpec("dollar", "imperial", 40, t["s"].strokes + (S((21, 118), (21, -18), kind="free"),), branch=False)

    return t
