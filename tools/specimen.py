#!/usr/bin/env python3
"""Generuje wzornik Kuropatwy: transliterator, klucz według warstw, zasady pisma.

Użycie:  python3 tools/specimen.py [plik_wyjściowy] [ścieżka_do_fontów]
Domyślnie: specimen/index.html z fontami z ../dist/
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kuropatwa.charset import REQUIRED  # noqa: E402
from kuropatwa.glyphs import glyph_table  # noqa: E402

LAYERS = [
    ("core", "Rdzeń Corvum",
     "Proste rysy dziobem, bez łuków. Krukowate zaproponowały wspólny język i dały mu pierwsze znaki."),
    ("mammal", "Dopisek ssaków",
     "Głoski wargowe. Znak bezwargowego odpowiednika plus łuk warg: m←n, p←t, b←d, f←h, w←ł. "
     "Ptak, który pominie łuk, przeczyta formę zredukowaną."),
    ("nasal", "Nosówki", "ą i ę: samogłoska z ogonem pod linię."),
    ("loxodon", "Belka Loxodon",
     "Umlauty ä ö ü. Ciężka belka nad gałęzią oznacza zapożyczenie instytucjonalne, jak w ogä."),
    ("imperial", "Dopiski imperialne",
     "Litery i akcenty do zapisu imion ludzkich. Haczyk obcości nad gałęzią zdradza pochodzenie."),
    ("punct", "Interpunkcja", "Kropka zamyka, dwukropek otwiera wypowiedź. ! i ? przebijają gałąź w górę."),
    ("digit", "Cyfry", "Pień i nacięcia. 5 (lin, „ciąć”) to cięcie przez pień, 0 (nol, „pustka”) to pusty romb."),
]

OATH = """kosen, ogä!! kornik. kosen, kösal.
na = !jack! durtan-in !thorlene!, sekorat.
na kir-ło kate. sena na kir-ka-ło sete.
sete !nain norat-or. saor = kakat-or.
na don donha saorsu.
na !tar saor nain salun-te.
saorin kat = nain kat. saorin nork = nain nork.
!thorlene!-or = gorat-ir.
na lan lanka: tekan, donat, durol.
norha tior: saor kir-ka-ha tekor-su.
kosun."""

PAGE = r"""<title>Kuropatwa</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,600;1,400&family=Alegreya+Sans+SC:wght@500;700&display=swap">
<style>
@font-face { font-family: "Kuropatwa"; src: url("__FONTS__kuropatwa.woff2") format("woff2"), url("__FONTS__kuropatwa.woff") format("woff"); font-display: block; }
@font-face { font-family: "Kuropatwa Drap"; src: url("__FONTS__kuropatwa-drap.woff2") format("woff2"), url("__FONTS__kuropatwa-drap.woff") format("woff"); font-display: block; }

/* Układ: kartka z archiwum Corvum. Wąska kolumna tekstu, szeroki pas pisma, klucz jako tablica warstw. */
:root {
  --bg: #e9ece6;        /* kora brzozy, chłodna */
  --paper: #f6f7f3;
  --ink: #1c2422;
  --muted: #5d6763;
  --rule: #c9cfc8;
  --accent: #3e6b5a;    /* mech */
  --l-core: #1c2422; --l-mammal: #4f7a3a; --l-nasal: #8a5a1c; --l-loxodon: #5a5f86;
  --l-imperial: #9b3b36; --l-punct: #5d6763; --l-digit: #2f6276;
  --f-body: "Alegreya", Georgia, serif;
  --f-label: "Alegreya Sans SC", "Alegreya", sans-serif;
  --f-k: "Kuropatwa", serif;
  --f-kd: "Kuropatwa Drap", "Kuropatwa", serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #131917; --paper: #1a2220; --ink: #dfe6e1; --muted: #93a09a; --rule: #2d3834; --accent: #8fc0a8;
  --l-core: #dfe6e1; --l-mammal: #9fca86; --l-nasal: #e0a85c; --l-loxodon: #a9addb;
  --l-imperial: #e88a83; --l-punct: #93a09a; --l-digit: #7fbfd6; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #131917; --paper: #1a2220; --ink: #dfe6e1; --muted: #93a09a; --rule: #2d3834; --accent: #8fc0a8;
  --l-core: #dfe6e1; --l-mammal: #9fca86; --l-nasal: #e0a85c; --l-loxodon: #a9addb;
  --l-imperial: #e88a83; --l-punct: #93a09a; --l-digit: #7fbfd6; color-scheme: dark; }

* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 17px/1.55 var(--f-body); margin: 0; }
.wrap { max-width: 1080px; margin: 0 auto; padding-block: 40px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 56px; }
.label { font-family: var(--f-label); font-weight: 700; letter-spacing: .06em; font-size: 13px; color: var(--muted); }
h1, h2 { font-weight: 600; text-wrap: balance; margin: 0; }
h2 { font-size: 26px; }
p { margin: 0; max-width: 65ch; }

header { display: grid; gap: 12px; }
.title-k { font-family: var(--f-kd); font-size: clamp(64px, 14vw, 148px); line-height: 1.25; color: var(--ink); overflow-wrap: anywhere; }
header h1 { font-size: 22px; }
header h1 span { color: var(--muted); font-weight: 400; }

/* transliterator */
.tool { background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; display: grid; gap: 0; }
.controls { display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center; padding: 14px 18px; border-bottom: 1px solid var(--rule); }
.seg { display: inline-flex; border: 1px solid var(--rule); border-radius: 4px; overflow: hidden; }
.seg button { font: 600 14px var(--f-body); background: transparent; color: var(--muted); border: 0; padding: 6px 12px; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--paper); }
.controls label { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; color: var(--muted); }
input[type=range] { accent-color: var(--accent); width: 130px; }
button:focus-visible, textarea:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.panes { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr); }
@media (max-width: 760px) { .panes { grid-template-columns: minmax(0, 1fr); } }
textarea { width: 100%; min-height: 320px; resize: vertical; border: 0; border-right: 1px solid var(--rule);
  background: transparent; color: var(--ink); font: 16px/1.7 var(--f-body); padding: 16px 18px; }
@media (max-width: 760px) { textarea { border-right: 0; border-bottom: 1px solid var(--rule); min-height: 180px; } }
.out { padding: 18px; display: grid; gap: 14px; align-content: start; min-width: 0; overflow-x: auto; }
.line { display: grid; gap: 2px; }
.line .k { font-family: var(--f-k); line-height: 1.3; white-space: pre-wrap; overflow-wrap: anywhere; }
.drap .line .k { font-family: var(--f-kd); }
.line .lat { font-size: 13px; color: var(--muted); }
.nogloss .line .lat { display: none; }

/* klucz */
.layers { display: grid; gap: 36px; }
.layer { display: grid; grid-template-columns: minmax(0, 260px) minmax(0, 1fr); gap: 24px; padding-top: 18px; border-top: 1px solid var(--rule); }
@media (max-width: 760px) { .layer { grid-template-columns: minmax(0, 1fr); } }
.layer h3 { margin: 0 0 6px; font-size: 19px; display: flex; align-items: center; gap: 10px; }
.layer h3 i { width: 12px; height: 12px; border-radius: 50%; background: var(--c); flex: none; }
.layer p { font-size: 15px; color: var(--muted); }
.cells { display: grid; grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); gap: 8px; }
.cell { display: grid; justify-items: center; gap: 2px; padding: 8px 4px 6px; background: var(--paper); border-radius: 4px; }
.cell .g { font-family: var(--f-k); font-size: 40px; line-height: 1.35; color: var(--c); }
.drapkey .cell .g { font-family: var(--f-kd); }
.cell .c { font-size: 14px; color: var(--muted); font-variant-numeric: tabular-nums; }

/* zasady */
.rules { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 28px 40px; }
.rule { display: grid; gap: 8px; align-content: start; }
.rule h3 { margin: 0; font-size: 18px; }
.rule .ex { font-family: var(--f-k); font-size: 30px; line-height: 1.4; }
.rule .ex + .label { margin-top: -6px; }
.rule p { font-size: 15.5px; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88em; background: var(--paper); padding: 1px 5px; border-radius: 3px; }
pre { background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: 14px 16px; overflow-x: auto; font-size: 13.5px; margin: 0; }
footer { color: var(--muted); font-size: 14px; display: grid; gap: 12px; }
</style>

<div class="wrap">
  <header>
    <div class="label">Pismo Birdfolk · Wspólny Zwierzoludzki</div>
    <div class="title-k" aria-hidden="true">kuropatwa</div>
    <h1>Kuropatwa <span>· pismo, które zaczęli Corvum, a dopisali wszyscy</span></h1>
    <p>Litery wiszą pod gałęzią jak ptak na żerdzi, a gałąź ciągnie się przez całe słowo, bo w Birdfolku ciągłość mowy ma pierwszeństwo. Spacja przerywa gałąź. Wielkich liter nie ma, więc nikt nie jest zapisany jako ważniejszy.</p>
    <p>Pisze się ją piórem albo pazurem. Pióro daje gładką kreskę w listach i księgach, pazur kilka równoległych rys w korze, drewnie i kamieniu.</p>
  </header>

  <section class="tool" aria-label="Transliterator">
    <div class="controls">
      <div class="seg" role="group" aria-label="Styl">
        <button id="st-clean" type="button" aria-pressed="true" title="Kuropatwa (Czysty)">Pióro</button>
        <button id="st-drap" type="button" aria-pressed="false" title="Kuropatwa Drap">Pazur</button>
      </div>
      <label for="size">Rozmiar <input id="size" type="range" min="18" max="96" value="34"></label>
      <label for="gloss"><input id="gloss" type="checkbox" checked> Podpis łaciński</label>
    </div>
    <div class="panes">
      <textarea id="src" spellcheck="false" aria-label="Tekst do zapisania">__OATH__</textarea>
      <div id="out" class="out" aria-live="polite"></div>
    </div>
  </section>

  <section class="layers" aria-labelledby="key-h">
    <div style="display:flex;flex-wrap:wrap;gap:12px 24px;align-items:baseline;justify-content:space-between">
      <h2 id="key-h">Klucz według warstw</h2>
      <div class="seg" role="group" aria-label="Styl klucza">
        <button id="k-clean" type="button" aria-pressed="true" title="Kuropatwa (Czysty)">Pióro</button>
        <button id="k-drap" type="button" aria-pressed="false" title="Kuropatwa Drap">Pazur</button>
      </div>
    </div>
    <div id="key" class="layers"></div>
  </section>

  <section aria-labelledby="rules-h" style="display:grid;gap:24px">
    <h2 id="rules-h">Zasady zapisu</h2>
    <div class="rules">
      <div class="rule"><h3>Imię i ród przez !</h3>
        <div class="ex">!jack! !thorlene! !!leothern!!</div><div class="label">!jack! · !thorlene! · !!leothern!!</div>
        <p>Imię własne bez znacznika jest niewidzialne. Pojedyncze <code>!</code> otacza imię i ród, podwójne prawdziwe imię wypowiadane w pełnym zaufaniu.</p></div>
      <div class="rule"><h3>Ruchomy akcent</h3>
        <div class="ex">!jack! !tam poszedł</div><div class="label">!jack! !tam poszedł</div>
        <p><code>!</code> przed słowem robi z niego akcent zdania, <code>?</code> pyta właśnie o nie. Oba przebijają gałąź w górę.</p></div>
      <div class="rule"><h3>Łącznik to goła gałąź</h3>
        <div class="ex">ne-kir-ka-ło</div><div class="label">ne-kir-ka-ło · nie doszedł</div>
        <p>Granica morfemów nie przerywa słowa. Między rdzeniem a końcówką biegnie sama gałąź.</p></div>
      <div class="rule"><h3>Cyfry stoją osobno</h3>
        <div class="ex">1 2 3 4 5 6 7 8 9 0</div><div class="label">un do tre kar lin son sat tok … nol</div>
        <p>Liczby nie wiszą pod gałęzią. Nacięcia liczy się od góry, cięcie przez pień dodaje pięć.</p></div>
    </div>
  </section>

  <footer>
    <h2 style="color:var(--ink);font-size:20px">Wpięcie na stronę</h2>
    <p>Skopiuj pliki z <code>dist/</code> obok strony i dołącz arkusz:</p>
    <pre>&lt;link rel="stylesheet" href="kuropatwa.css"&gt;
&lt;span class="kuropatwa"&gt;kosen, !ogä!! kornik.&lt;/span&gt;
&lt;span class="kuropatwa-drap"&gt;kosun.&lt;/span&gt;</pre>
    <p>Kształty liter są własne. Humblescratch (Hit Point Press) żyje w świecie gry jako dawne pismo ceremonialne, ale nie jest częścią tego fontu.</p>
  </footer>
</div>

<script>
const KEY = __KEY__;
const LAYERS = __LAYERS__;
const $ = (s) => document.querySelector(s);
const src = $("#src"), out = $("#out"), size = $("#size"), gloss = $("#gloss");

function renderOut() {
  out.replaceChildren(...src.value.split("\n").map((t) => {
    const line = document.createElement("div"); line.className = "line";
    const k = document.createElement("div"); k.className = "k"; k.textContent = t || " ";
    k.style.fontSize = size.value + "px";
    const lat = document.createElement("div"); lat.className = "lat"; lat.textContent = t;
    line.append(k, lat); return line;
  }));
}
function seg(a, b, on) {
  a.setAttribute("aria-pressed", String(on)); b.setAttribute("aria-pressed", String(!on));
}
$("#st-clean").onclick = () => { out.classList.remove("drap"); seg($("#st-clean"), $("#st-drap"), true); };
$("#st-drap").onclick = () => { out.classList.add("drap"); seg($("#st-clean"), $("#st-drap"), false); };
$("#k-clean").onclick = () => { $("#key").classList.remove("drapkey"); seg($("#k-clean"), $("#k-drap"), true); };
$("#k-drap").onclick = () => { $("#key").classList.add("drapkey"); seg($("#k-clean"), $("#k-drap"), false); };
gloss.onchange = () => out.classList.toggle("nogloss", !gloss.checked);
src.addEventListener("input", renderOut);
size.addEventListener("input", renderOut);

const key = $("#key");
for (const [id, name, desc] of LAYERS) {
  const chars = KEY.filter((k) => k[1] === id);
  if (!chars.length) continue;
  const sec = document.createElement("div"); sec.className = "layer";
  sec.style.setProperty("--c", `var(--l-${id})`);
  sec.innerHTML = `<div><h3><i></i></h3><p></p></div><div class="cells"></div>`;
  sec.querySelector("h3").append(name); sec.querySelector("p").textContent = desc;
  const cells = sec.querySelector(".cells");
  for (const [ch] of chars) {
    const c = document.createElement("div"); c.className = "cell";
    c.innerHTML = `<span class="g" aria-hidden="true"></span><span class="c"></span>`;
    c.firstChild.textContent = ch; c.lastChild.textContent = ch;
    cells.append(c);
  }
  key.append(sec);
}
renderOut();
</script>
"""


STANDALONE = """<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head><body>
{page}
</body></html>
"""


def build(out: Path, fonts: str, standalone: bool = True) -> Path:
    table = glyph_table()
    key = [[c, table[c].layer] for c in REQUIRED]
    page = (PAGE.replace("__FONTS__", fonts)
            .replace("__OATH__", html.escape(OATH))
            .replace("__KEY__", json.dumps(key, ensure_ascii=False))
            .replace("__LAYERS__", json.dumps(LAYERS, ensure_ascii=False)))
    if standalone:
        page = STANDALONE.format(page=page)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "specimen/index.html"
    fonts = sys.argv[2] if len(sys.argv) > 2 else "../dist/"
    # trzeci argument "fragment": bez szkieletu dokumentu (do publikacji jako Artifact)
    print(build(out, fonts, standalone=not (len(sys.argv) > 3 and sys.argv[3] == "fragment")))
