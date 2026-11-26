"""Zamiana szkieletów kresek na kontury glifu (font units)."""
from __future__ import annotations

import math
import random
import zlib

import pathops

from .glyphs import GlyphSpec, Stroke

GRID = 7           # font units na jednostkę siatki
PAD = 9            # margines boczny w siatce (gałąź go wypełnia)
BRANCH_Y = 100

WIDTH = {          # (szerokość na początku, szerokość na końcu) w font units
    "hang": (92, 22),
    "free": (76, 20),
    "mark": (84, 30),
    "bar": (92, 92),
    "branch": (64, 64),
}


def advance(spec: GlyphSpec) -> int:
    return round((spec.width + 2 * PAD) * GRID)


def _poly_area(poly):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1])) / 2


def _add(path: pathops.Path, poly):
    pts = [(round(x), round(y)) for x, y in poly]
    if abs(_poly_area(pts)) < 1:
        return
    if _poly_area(pts) < 0:
        pts.reverse()
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    path.close()


def _disc(c, r, n=12):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _ribbon(path: pathops.Path, pts, w0: float, w1: float, taper_start: bool, tip: bool = True):
    """Wstęga o szerokości zmieniającej się liniowo od w0 do w1 wzdłuż łamanej."""
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(lens) or 1.0
    acc = 0.0
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        if L == 0:
            continue
        t0, t1 = acc / total, (acc + L) / total
        acc += L
        wa = w0 + (w1 - w0) * t0
        wb = w0 + (w1 - w0) * t1
        if taper_start:  # oba końce zwężone (rysa „free”)
            wa = min(wa, w1 + (w0 - w1) * min(1, t0 * 4))
            wb = min(wb, w1 + (w0 - w1) * min(1, t1 * 4))
        nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
        _add(path, [
            (a[0] + nx * wa / 2, a[1] + ny * wa / 2),
            (b[0] + nx * wb / 2, b[1] + ny * wb / 2),
            (b[0] - nx * wb / 2, b[1] - ny * wb / 2),
            (a[0] - nx * wa / 2, a[1] - ny * wa / 2),
        ])
        if t1 < 0.999:  # łagodny węzeł między odcinkami
            _add(path, _disc(b, wb / 2))
    if not tip:
        return
    # ostry czubek na końcu: trójkąt wydłużający rysę
    a, b = pts[-2], pts[-1]
    L = math.dist(a, b) or 1.0
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    _add(path, [(b[0] - uy * w1 / 2, b[1] + ux * w1 / 2), (b[0] + ux * w1 * 1.4, b[1] + uy * w1 * 1.4),
                (b[0] + uy * w1 / 2, b[1] - ux * w1 / 2)])


def _to_units(stroke: Stroke) -> list[tuple[float, float]]:
    return [((x + PAD) * GRID, y * GRID) for x, y in stroke.pts]


def _clean(path, pts, kind):
    w0, w1 = WIDTH[kind]
    if kind in ("bar", "branch"):
        _ribbon(path, pts, w0, w0, False, tip=False)
    elif kind in ("hang", "mark"):
        _ribbon(path, pts, w0, w1, False)
    else:
        _ribbon(path, pts, w0, w1, True)


def _drap(path, pts, kind, rng: random.Random):
    """Faktura drapana: 2–3 włoskowate rysy wzdłuż szkieletu z drobnym rozchwianiem."""
    w0, _ = WIDTH[kind]
    n = 2 if kind == "branch" else 3
    hair = w0 * 0.44
    for i in range(n):
        off = (i - (n - 1) / 2) * w0 * 0.36
        jit = []
        for j, (x, y) in enumerate(pts):
            end = j in (0, len(pts) - 1)
            if kind == "branch":
                dx, dy = 0.0, (0.0 if end else rng.uniform(-6, 6))
            else:
                dx, dy = rng.uniform(-7, 7), rng.uniform(-7, 7)
            jit.append((x + dx, y + dy))
        # przesunięcie prostopadłe do pierwszego odcinka
        a, b = jit[0], jit[1]
        L = math.dist(a, b) or 1.0
        nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
        line = [(x + nx * off, y + ny * off) for x, y in jit]
        if kind != "branch":  # rysy różnej długości
            k = rng.uniform(0.0, 0.12)
            a, b = line[-2], line[-1]
            line[-1] = (b[0] - (b[0] - a[0]) * k, b[1] - (b[1] - a[1]) * k)
        flat = kind in ("bar", "branch")
        _ribbon(path, line, hair, hair if flat else hair * 0.3, kind == "free", tip=not flat)


def render(spec: GlyphSpec, style: str = "clean", seed: int = 0) -> pathops.Path:
    if style not in ("clean", "drap"):
        raise ValueError(style)
    path = pathops.Path()
    rng = random.Random(zlib.crc32(spec.name.encode()) ^ seed)
    items = [(_to_units(s), s.kind) for s in spec.strokes]
    if spec.branch:
        adv = advance(spec)
        items.insert(0, ([(-4.0, BRANCH_Y * GRID), (adv + 4.0, BRANCH_Y * GRID)], "branch"))
    for pts, kind in items:
        if style == "clean":
            _clean(path, pts, kind)
        else:
            _drap(path, pts, kind, rng)
    return pathops.simplify(path, fix_winding=True, clockwise=True)
