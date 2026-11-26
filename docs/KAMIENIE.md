# Kamienie milowe: Kuropatwa

Dziennik decyzji i postępów, żeby żaden czat nie gubił ciągłości.

## Hierarchia czatów
- **Język Birdfolk** (słowa, dźwięki, ortografia): czat/repo **Whitewood**. Tutaj tylko odczyt.
- **Pismo Kuropatwa** (kształty, font): **to repo**. Zmiany kształtów robimy wyłącznie tutaj.
- Wpięcie fontu w stronę Whitewood: czat Whitewood, na podstawie plików z `dist/`.

## Ustalenia
- 2026-11-26: Własne pismo, nie Humblescratch. Powód: licencja Hit Point Press zabrania
  webfontu i rozpowszechniania. Pliki HPP nie trafiają do repo.
- 2026-11-26: Kuropatwa ewoluowała: rdzeń od Corvum, potem dopiski innych grup
  (warstwy opisane w specyfikacji).
- 2026-11-26: Ród Jacka w Whitewood to `!thorlene!`. `!leothern!` występuje w dokumencie
  języka jako imię rodowe (prawdziwe). W tekstach przykładowych używamy `thorlene`.
- 2026-11-26: Wybrane podejście A (generator w Pythonie). Randomizacja odręczności
  to kolejny etap.

- 2026-11-26: Litery wiszą pod **gałęzią** łączącą słowo (lore: „ciągłość mowy ma pierwszeństwo”).
  Spółgłoski pełnej wysokości, samogłoski krótkie, `!`/`?` przebijają gałąź w górę, `-` to goła
  gałąź, spacja ją przerywa. Cyfry stoją bez gałęzi.
- 2026-11-26: Wargowe = bezwargowy partner + łuk warg (m←n, p←t, b←d, f←h, w←ł, wg tablicy
  konwersji z dokumentu języka). Dźwięczność = podeszwa (t→d, k→g, s→z). x = zrost k+s.
- 2026-11-26: Rozróżnialność: różne podstawy ≥3 wyraźne piksele w 16 px, dopiski ≥6 w 24 px.
  Progi skalibrowane na powiększonym podglądzie 16 px (d/t, l/ł, cyfry czytelne gołym okiem).
- 2026-11-26: Porównanie z Humblescratch litera w literę (lokalnie, plik HPP poza repo):
  żaden kształt się nie pokrywa.

- 2026-11-26: **Lore narzędzi:** `Kuropatwa` (Czysty) = zapis **piórem**, `Kuropatwa Drap` = zapis
  **pazurem**. Opis w `docs/LORE-pismo.md`. Przyciski wzornika: Pióro / Pazur.
- 2026-11-26 (Krąg Cieni, zatwierdzone przez MG): Whitewood rozwijało się **niezależnie od
  Imperium**, ale na podobnym poziomie technologicznym. Możliwy wynalazek niezależny także
  w piśmie.

## Otwarte
- **Przegląd warstwy imperialnej.** W v0.1 do „imperialnych” trafiło wszystko, czego nie
  wyjaśniał rdzeń (`q v x y ß` i akcenty romańskie), bez oparcia w rozdziale „Wkłady językowe
  grup”. Ten rozdział wskazuje innych autorów:
  - `y` jest rdzenne: epenteza `y` to reguła konwersji wargowych (łyspólnota, nygła);
  - akcenty francuskie (`é è ê ç`): Vulpin (40% francuskie), Luma (30% francuskie);
  - akcenty włoskie i hiszpańskie (`à ì ò ù ñ`): Luma, Harengon (włoskie południowe);
  - akcenty portugalskie (`ã ç á`): wodne, Hedge;
  - `ß`: Mapach (niemieckie kupieckie). Hedge nie, bo szwajcarski niemiecki nie używa ß;
  - zostają imperialne: `q x v`, do imion ludzkich.
  Do zbadania: co D&D mówi o pismach innych ras (Common, Elvish/Espruar, Dwarvish/Dethek,
  Infernal, Draconic…), żeby ustalić, które znaki mogły dotrzeć z zewnątrz, a które powstały
  niezależnie.

## Postęp
- [x] Specyfikacja: `docs/superpowers/specs/2026-11-26-kuropatwa-webfont-design.md`
- [x] Zatwierdzenie specyfikacji
- [x] Generator + styl czysty (v0.1.0)
- [x] Styl Drap
- [x] Wzornik + transliterator (`specimen/index.html`, artifact: https://claude.ai/artifact/GzU4ZCgr8KSaRHAMLv6HAX)
- [ ] Randomizacja (warianty + `calt`)
- [ ] Wpięcie w stronę Whitewood (czat Whitewood)
