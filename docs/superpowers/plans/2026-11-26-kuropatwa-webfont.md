# Kuropatwa Webfont Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generator w Pythonie budujący webfont Kuropatwa (styl czysty + Drap) z danych o szkieletach kresek, plus wzornik z transliteratorem.

**Architecture:** Szkielety znaków (łamane/łuki w siatce) → renderer kresek (kontury, scalanie skia-pathops) → fontTools FontBuilder (TrueType) → TTF/WOFF/WOFF2 + CSS + wygenerowany `specimen/index.html`. Style różnią się tylko rendererem kreski; losowość deterministyczna.

**Tech Stack:** Python 3.11+, fontTools, skia-pathops, brotli, Pillow (testy rozróżnialności), pytest.

**Spec:** `docs/superpowers/specs/2026-11-26-kuropatwa-webfont-design.md`

## Global Constraints

- Zestaw znaków dokładnie wg spec pkt 2; wielkie litery → ten sam glif co małe.
- UPM 1000; wysokość ciała znaku 700 (siatka ×7); dopiski do 1000; ogonki do −200.
- Warstwy: `core`, `mammal`, `nasal`, `loxodon`, `imperial`, `punct`, `digit` — każdy glif ma dokładnie jedną.
- Rdzeń (`core`): wyłącznie odcinki proste. `mammal`: dokładnie jeden łuk.
- `ä ö ü` = samogłoska + belka (nie kropki). Cyfry: pień + nacięcia, 5 = cięcie skośne, 0 = romb.
- Nazwy rodzin: `Kuropatwa` i `Kuropatwa Drap`. Pliki: `dist/kuropatwa.{ttf,woff,woff2}`, `dist/kuropatwa-drap.{ttf,woff,woff2}`, `dist/kuropatwa.css`.
- Żadnych plików Hit Point Press w repo.

## Review Focus

1. Pomylenie glifów w 16 px → test rozróżnialności na bitmapach (Task 4).
2. Tekst wpisany WIELKIMI / z polskimi wielkimi (`Ą`, `Ł`) → cmap mapuje (Task 4).
3. Znak spoza zestawu (np. `"`, `—`) → przeglądarka spada na font zapasowy; CSS deklaruje `unicode-range`? Nie — zwykły fallback w stosie `font-family` (Task 5 CSS).
4. Przebudowa daje inny Drap → test deterministyczności (Task 4).
5. Nakładające się kreski dają dziury przy renderowaniu → scalanie pathops + test „brak samoprzecięć” (Task 2).

---

### Task 1: Zestaw znaków i dane glifów

**Files:**
- Create: `src/kuropatwa/__init__.py`, `src/kuropatwa/charset.py`, `src/kuropatwa/glyphs.py`
- Test: `tests/test_glyphs.py`

**Interfaces:**
- Produces: `charset.REQUIRED: str` (wszystkie znaki ze spec), `glyphs.glyph_table() -> dict[str, GlyphSpec]`;
  `GlyphSpec(name: str, layer: str, width: int, strokes: list[Stroke])`; `Stroke = list[tuple[float,float]] | Arc`;
  `Arc(cx, cy, r, a0, a1)` (stopnie). Współrzędne w siatce: 1 jednostka = 6 font units, y=0 linia bazowa, y=100 góra ciała.

- [ ] Test: `set(charset.REQUIRED) <= set(glyph_table())`; każda warstwa w zbiorze dozwolonym; glify `core` bez `Arc`; glify `mammal` mają dokładnie jeden `Arc`; żadne dwa glify nie mają identycznych `strokes`.
- [ ] Uruchom `pytest tests/test_glyphs.py` → FAIL.
- [ ] Implementacja: znaki bazowe jako dane; diakrytyki (`soft`, `voice`, `belka`, `ogonek`, `acute`, `grave`, `circ`, `tilde`, `cedilla`, `hook`) jako doklejane elementy przez `compose(base, *marks)`.
- [ ] `pytest` → PASS. Commit.

### Task 2: Renderer kresek

**Files:** Create `src/kuropatwa/render.py`; Test `tests/test_render.py`

**Interfaces:**
- Produces: `render(spec: GlyphSpec, style: str, seed: int = 0) -> pathops.Path` (`style` ∈ `"clean"`, `"drap"`), w font units, już scalony, kontury zgodnie z ruchem wskazówek (TrueType).

- [ ] Test: dla `a` w obu stylach ścieżka niepusta, bbox w granicach (y ≥ −160, y ≤ 820); `render(...)` dwukrotnie z tym samym seedem → identyczne kontury; drap z innym seedem → różne.
- [ ] FAIL → implementacja (odcinki jako czworokąty o szerokości zwężanej ku końcom, ostre zakończenia, wielokąt w węzłach; łuki próbkowane co 10°; drap = 3 włoskowate rysy z jitterem z `random.Random(seed ^ hash(name))`) → PASS. Commit.

### Task 3: Budowa fontu

**Files:** Create `src/kuropatwa/build.py`, `tools/build.py`; Test `tests/test_build.py`

**Interfaces:**
- Produces: `build_font(style: str) -> TTFont`; `write_all(out_dir: Path) -> list[Path]` (TTF/WOFF/WOFF2 dla obu stylów + CSS).

- [ ] Test: cmap zawiera `REQUIRED` oraz `ch.upper()` dla każdej litery, wskazując ten sam glif; `write_all(tmp)` tworzy 7 plików; WOFF2 otwiera się przez `TTFont`.
- [ ] FAIL → implementacja (FontBuilder, TTGlyphPen, metryki, name table, `.notdef`, `space`) → PASS. Commit.

### Task 4: Kontrola jakości

**Files:** Create `tests/test_quality.py`, `tools/preview.py`

- [ ] Test rozróżnialności: każdy glif wyrenderowany Pillowem z TTF w 16 px; minimalna odległość Hamminga między parami bitmap > 6 px (z wyjątkiem par z `ALLOWED_SIMILAR`, pustej domyślnie).
- [ ] Test deterministyczności: dwa `build_font("drap")` → identyczne tablice `glyf`.
- [ ] `tools/preview.py` → `docs/preview.png` (tabela klucza do oceny wzrokowej). Ocena wzrokowa, poprawki kształtów w Task 1 aż testy i oko przejdą. Commit.

### Task 5: Wzornik i transliterator

**Files:** Create `tools/specimen.py` (generuje `specimen/index.html`), modyfikuje `write_all` tak, by wołał generator.

- [ ] Strona: `@font-face` z `../dist/`, tabela klucza pogrupowana i pokolorowana warstwami, przysięga Jacka (`!thorlene!`), pole tekstowe z podglądem na żywo w obu stylach, suwak rozmiaru. Jasny/ciemny motyw. Działa z `file://`.
- [ ] Sprawdzenie: Playwright otwiera stronę, wpisuje `kosen, !ogä!! kornik.`, zrzut ekranu; fonty załadowane (`document.fonts.check`).
- [ ] Commit; aktualizacja `docs/KAMIENIE.md`, README (jak budować, jak wpiąć CSS); push.
