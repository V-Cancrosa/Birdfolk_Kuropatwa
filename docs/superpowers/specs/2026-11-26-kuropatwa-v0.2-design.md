# Kuropatwa v0.2 (projekt)

Data: 2026-11-26 · Status: **projekt na piśmie, nic nie budujemy przed zatwierdzeniem**

Dotyczy fontu z v0.1 (`docs/superpowers/specs/2026-11-26-kuropatwa-webfont-design.md`).
Część A jest do zatwierdzenia. Część B czeka na decyzje.

---

## A. Myślnik: dwie role jednego znaku

### Ustalenie (od autora języka)

W rodzimym zapisie Birdfolk **morfemy są zrośnięte**: pisze się `nanenir`, nie `na-ne-nir`.
Użytkownicy języka sami rozpoznają zbitkę morfemów i sylab. Łącznik w zapisie `na-ne-nir` to
**pomoc dla uczącego się** (polskiego czytelnika, graczy, autora), a nie część rodzimej
ortografii.

Dokument języka (konwencje typograficzne) przewiduje też **myślnik jako punkt wyliczenia**:
„Wyliczenia z myślnikiem (-)”. Znak `-` (U+002D) ma więc w praktyce dwie role, a v0.1 rysuje
obie jako gołą gałąź. Dla wyliczeń to błąd, bo punkt listy musi być widoczny i nie może łączyć
się z następnym słowem.

### Projekt

Font sam rozpoznaje rolę po sąsiedztwie (OpenType `calt`, w przeglądarkach włączone domyślnie).

| Kontekst | Rola | Glif | Wygląd |
|---|---|---|---|
| `-` **między znakami słowa** (`na-ne-nir`, `kir-ka-ło`, `!thorlene!-or`) | podział morfemów dla uczącego się | `hyphen.morph` | goła gałąź na całą szerokość, łączy się z sąsiadami (jak w v0.1) |
| `-` **w każdym innym miejscu** (początek linii, po spacji: `- tekan`) | rodzimy punkt wyliczenia | `hyphen` (domyślny) | **gałązka**: krótki, odcięty odcinek gałęzi z małym sękiem, z odstępem po obu stronach |
| `–` (U+2013, półpauza) | wymuszony punkt wyliczenia | `hyphen` | jak wyżej, bez względu na kontekst |

**Znaki słowa** (klasa kontekstu): wszystkie litery, `!` i `?`, bo znaczniki imienia i akcentu są
częścią słowa (`!thorlene!-or`). Cyfry nie należą do słowa: `3-5` daje punkt wyliczenia
(zakresów dokument języka nie opisuje, więc nie zgadujemy).

**Reguła (kierunek):** domyślnie widoczny punkt wyliczenia. Podstawienie na `hyphen.morph`
następuje tylko wtedy, gdy z obu stron stoi znak słowa. Błąd w tę stronę jest bezpieczniejszy:
źle rozpoznany łącznik pokaże się jako widoczny znak, a nie zniknie.

**Kształt gałązki:** odcinek na wysokości gałęzi, szerokość ok. 30 jednostek siatki, z
marginesami, więc **nie dotyka** gałęzi sąsiednich słów. Mały sęk to krótki zadzior w dół, wyraźnie
krótszy niż samogłoska `e`, żeby się z nią nie mylił. W zapisie pazurem gałązka dostaje tę samą
fakturę co reszta.

**Rodzimy zapis bez łączników** niczego nie wymaga: `nanenir` już dziś daje jedną ciągłą gałąź.

### Lore (do `docs/LORE-pismo.md`)

- Birdfolk pisze słowo jako jedną gałąź, a morfemy zrastają się bez śladu.
- Łącznik `-` między morfemami to notacja dla obcych (polska transkrypcja). W piśmie widać go
  jako odsłonięty kawałek gałęzi, jakby ktoś zdjął z niej literę.
- Wyliczenie to odcięta gałązka z sękiem, położona przed pozycją listy.

### Do przekazania czatowi Whitewood (właściciel języka)

Ustalenie o zrośniętych morfemach dotyczy ortografii, więc powinno trafić do dokumentu języka.
Przykłady w dokumencie (`kir-ka-ło`, `donor-ko-or-in`) to transkrypcja dla uczącego się, a nie
zapis rodzimy. Proponowany dopisek do rozdziału „Konwencje typograficzne”:
*„Łącznik między morfemami to wyłącznie notacja transkrypcyjna. Pismo rodzime zrasta morfemy.”*

### Zmiany w repo (po zatwierdzeniu)

| Plik | Zmiana |
|---|---|
| `src/kuropatwa/glyphs.py` | glif `hyphen` = gałązka z sękiem (bez gałęzi na pełną szerokość), nowy `hyphen.morph` = goła gałąź (dzisiejszy `-`); `–` → `hyphen` |
| `src/kuropatwa/build.py` | tablica `GSUB` z `calt`: `@slowo hyphen' @slowo → hyphen.morph`; klasa `@slowo` z tabeli glifów (litery + `!` `?`) |
| `tests/test_shaping.py` | kształtowanie przez HarfBuzz (`uharfbuzz`, nowa zależność testów): `na-ne-nir` → 2× `hyphen.morph`; `- tekan` → `hyphen`; `!thorlene!-or` → `hyphen.morph`; `3-5` → `hyphen`; `nanenir` bez myślników |
| `tests/test_quality.py` | gałązka odróżnialna od `e` i `.` w 16 px |
| `tools/specimen.py` | zasada „Łącznik”: obok siebie `nanenir` (rodzimy) i `na-ne-nir` (dla uczącego się) oraz przykład listy |
| `docs/LORE-pismo.md`, `docs/KAMIENIE.md` | lore jak wyżej, decyzja w dzienniku |

### Anty-cele

- Rodzimy tekst bez łączników wygląda inaczej niż dziś.
- Punkt listy łączy się z następnym słowem albo znika.
- Reguła zależy od ustawień przeglądarki, które użytkownik musi włączać ręcznie.

---

## B. Przebudowa warstw dopisków (propozycja, czeka na decyzje)

Kontekst: Krąg Cieni to homebrew, Imperium pisze **Commonem**. Whitewood rozwijało się
niezależnie, więc akcenty to wynalazek grup z Whitewood, a ich podobieństwo do znaków imperialnych
to zbieżność. Dopisek należy do grupy, która go wymyśliła. Grupy ptasie piszą prostą rysą,
ssacze łukiem (wyjątek: belka Loxodon).

| Dopisek | Grupa | Kształt | Znaki |
|---|---|---|---|
| kreska pionowa | rdzeń | rysa pionowa | `ć ń ś ź` + `ó` |
| ostry | Luma | rysa skośna | `á é í ú` |
| ciężki | Harengon | łuk-zamach | `à è ì ò ù` |
| daszek | Vulpin | łuk-kita (∩) | `â ê î ô û` |
| cedylla | Vulpin | kita pod linią | `ç` |
| fala | wodne | zygzak | `ã ñ` |
| belka | Loxodon | ciężka belka | `ä ö ü` |
| zrost | Mapach | dwa `s` spięte łukiem | `ß` |
| haczyk obcości | Imperium (Common) | flaga nad gałęzią | `q x v` |

Inne zmiany: `y` przechodzi do rdzenia i traci haczyk (epenteza `y` to reguła języka).

**Pytania otwarte:**
1. Czy dopisek oznacza pochodzenie słowa (jak `ä`: zapożyczenie od Loxodon)? To decyzja
   o języku, więc trafiłaby do czatu Whitewood.
2. `ñ`: wodni (kształt fali) czy Luma (wpływ hiszpański)? Propozycja: wodni.
3. Czy dopisek grupy przeszedł na wszystkie samogłoski standardu? Propozycja: tak.

## Odrzucone

- **Piętrowe morfemy (okurigana)**: standard zostaje liniowy. Ewentualny dworski zapis
  Vulpinów to temat na atlas gwary Vulpin.
