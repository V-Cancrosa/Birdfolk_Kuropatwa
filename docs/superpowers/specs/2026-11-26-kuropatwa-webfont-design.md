# Kuropatwa: webfont pisma Birdfolk (projekt)

Data: 2026-11-26 · Status: **do zatwierdzenia**

## Po co

Kuropatwa to pismo języka Birdfolk (Wspólny Zwierzoludzki) z kampanii Whitewood.
Pierwszy cel: Jack (Vulpin z rodu `!thorlene!`) i stół D&D, czyli handouty, notatki,
przysięgi i strona Whitewood. Drugi cel: wspólne pismo wszystkich ras z taksonomii
języka.

Pisanie ma być wygodne jak każdym fontem: wpisujesz zwykły tekst (`kosen, !ogä!! kornik.`),
a na ekranie pojawiają się znaki Kuropatwy.

## Lore, które font odwzorowuje

- Źródło prawdy o języku: `birdfolk_architektura_v2_1.pdf` (rozdz. VI–VIII), prowadzony w czacie
  / repo **Whitewood**. To repo jest właścicielem **pisma**, a język tylko odczytuje.
- Pismo ewoluowało tak jak mowa. **Zaczęło się od Corvum**, a potem każda grupa dopisała swoje.
  Imperium dodało znaki do imion ludzkich. Dzisiejszy stan to Kuropatwa.
- Humblescratch istnieje w świecie gry jako dawne pismo ceremonialne, ale **nasze kształty są
  własne**. Licencja Hit Point Press zabrania używania go jako webfontu i rozpowszechniania,
  dlatego jego pliki (`.otf`, PDF-y) **nie trafiają do repo** i nie kopiujemy z nich kształtów
  liter. Wspólne mają być tylko zasady ogólne: drapana kreska i brak łuków w rdzeniu.

## Cele

1. Webfont `Kuropatwa` (WOFF2 + WOFF + TTF) z plikiem CSS `@font-face`, gotowy do wpięcia
   w stronę Whitewood.
2. Pełny zestaw znaków z rozdz. VI:
   - `a–z`
   - `ą ć ę ł ń ó ś ź ż`
   - `ä ö ü ß`
   - `á é í ó ú à è ì ò ù â ê î ô û ñ ã ç`
   - `0–9`
   - `. , : ; ! ?`
   - `$ + - / =`
   - spacja
3. **Brak wielkich liter.** `A` i `a` (także `Ą`/`ą` itd.) wskazują ten sam znak, więc tekst
   pisany wielkimi literami też się wyświetli.
4. **Historia widoczna w kształcie.** Warstwy pochodzenia:

   | Warstwa | Kto | Znaki | Gramatyka kreski |
   |---|---|---|---|
   | Rdzeń | Corvum | spółgłoski bezwargowe `t k d g s z h n l ł r c j`, `ć ś ź ń ż`, samogłoski `a e i o u` | 2–3 proste rysy, ostre kąty, zero łuków (dziób) |
   | Ssacza | Beastfolk (mają wargi) | wargowe `m p b f w` | szkielet rdzenny + jeden **łuk** (łapa) |
   | Nosowa | polska warstwa rdzenna | `ą ę` | samogłoska + ogonek-rys w dół |
   | Instytucjonalna | Loxodon | `ä ö ü` | samogłoska + ciężka pozioma **belka** nad znakiem (trąba), nie kropki |
   | Imperialna | Imperium | `q v x y ß`, akcenty romańskie, `ó` | szkielet + mały **haczyk** „obcości”; akcenty jako krótkie rysy nad znakiem |

5. Gramatyczne `!` i `?` mają być wyraźne, wąskie i ciasno dosunięte do słowa
   (`!!leothern!!`, `?!jack!`). Muszą się odróżniać od `i`, `l` i `ł` w 16 px.
6. **Cyfry własne** (nie karby z Humblescratch). Pionowy pień plus nacięcia:
   - 1–4: tyle nacięć;
   - 5 (`lin`, które znaczy też „ciąć”): skośne cięcie przez pień;
   - 6–9: cięcie plus 1–4 nacięcia;
   - 0 (`nol`, „pustka”): pusty romb.
7. Dwa style:
   - **Kuropatwa** (czysty): czytelny od 14 px, do tekstu i podpisów pod nagłówkami.
   - **Kuropatwa Drap**: każda kreska złożona z 2–3 włoskowatych, lekko rozchwianych rys,
     do nagłówków i handoutów.
8. Strona-wzornik (`specimen/index.html`):
   - tabela klucza (litera → znak), pokolorowana według warstw;
   - przysięga Jacka jako przykład;
   - pole „wpisz tekst → zobacz w Kuropatwie” do robienia handoutów.

## Poza zakresem (na teraz)

- **Randomizacja** odręczności, czyli różne warianty tego samego znaku. To następny etap.
  Font dostanie 2–3 warianty znaku i funkcję OpenType `calt`, która je rotuje. Generator
  będzie od początku przygotowany na warianty (ziarno losowania osobne dla każdego wariantu).
- Ligatury dwuznaków (`cz dz dż sz rz ch`) jako osobne znaki. Do rozważenia razem z gwarami.
- Wpięcie fontu w stronę Whitewood. To zadanie czatu Whitewood. Tutaj dostarczamy pliki
  i fragment CSS.
- Licencja publiczna (np. SIL OFL). To decyzja Twoja; do czasu decyzji repo nie ma licencji
  otwartej.

## Anty-cele (porażka, nawet jeśli działa)

- Znaki, które da się pomylić ze sobą w 16 px.
- Kształty odczytywalne kluczem Humblescratch, czyli kopia cudzego pisma.
- Font, którego nie da się rozbudować bez przerysowania wszystkiego (punkt F.4 dokumentu
  języka zakłada dalszą rozbudowę).

## Podejścia (rozważone)

- **A. Generator w Pythonie.** Szkielety kresek w pliku danych, skrypt robi font.
  **Wybrane.** Daje powtarzalność, łatwą rozbudowę i drugi styl oraz warianty prawie za darmo.
- B. Ręcznie rysowane SVG. Większa swoboda, ale każda zmiana stylu to przerysowanie ~100 znaków.
- C. Twoje rysunki zwektoryzowane. Najbardziej osobiste, ale wymaga Twojej pracy. Później
  można je wpiąć w A jako podmianę pojedynczych znaków.

## Jak (ustalenia techniczne)

- `src/glyphs.py`: dane. Każdy znak to lista kresek (łamane i łuki) w siatce 0–100, plus
  znaczniki warstwy i nazwy. Diakrytyki są doklejane jako osobne elementy (kreska, belka,
  ogonek, haczyk), więc nowy znak z akcentem nie wymaga rysowania.
- `tools/build.py`:
  - zamienia kreski na kontury (zwężające się końce, jak rys pazurem);
  - scala nakładające się kształty (`skia-pathops`);
  - składa font (`fontTools.FontBuilder`, TrueType, 1000 jednostek/em);
  - zapisuje `dist/kuropatwa*.woff2|woff|ttf`, `dist/kuropatwa.css` i wzornik.
- Styl Drap: te same szkielety, inny renderer kreski. Losowość jest deterministyczna
  (stałe ziarno), więc każda przebudowa daje ten sam font.
- `tools/check.py`: test po budowie. Sprawdza, czy wszystkie znaki z rozdz. VI są w foncie,
  czy wielkie litery wskazują małe, i renderuje podgląd PNG do oceny wzrokowej.
- Pliki wynikowe w `dist/` są commitowane, żeby dało się je pobrać bez budowania.

## Zostawione budowniczemu (moje decyzje w trakcie)

- Konkretne kształty liter, w ramach gramatyki warstw i anty-celów.
- Metryki (wysokość znaku, odstępy) dobrane pod czytelność w 16 px.

## Kamienie milowe

Prowadzone w `docs/KAMIENIE.md`.
