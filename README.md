# Birdfolk · Kuropatwa

Font i alfabet **Kuropatwa**, pismo języka **Birdfolk** (Wspólny Zwierzoludzki) z kampanii
D&D *Krąg Cieni* (Whitewood). Inspiracją było pismo Humblescratch z Humblewood, ale kształty
liter są własne.

![Klucz Kuropatwy: każda litera w obu zapisach i przysięga Jacka](docs/preview.png)

## Czym jest Kuropatwa

- **Litery wiszą pod gałęzią,** która łączy całe słowo, bo w Birdfolku ciągłość mowy ma
  pierwszeństwo. Spacja przerywa gałąź, a `!` i `?` przebijają ją w górę.
- **Historię widać w kształcie znaków.** Rdzeń dali Corvum, potem dopisywały się inne grupy:
  ssaki dodały łuk warg, Loxodoni belkę nad umlautem.
- **Brak wielkich liter.** `A` i `a` wyglądają tak samo, bo nikt nie jest zapisany jako
  ważniejszy.
- **Dwa zapisy:** piórem (font `Kuropatwa`) i pazurem (font `Kuropatwa Drap`).

Więcej: [`docs/LORE-pismo.md`](docs/LORE-pismo.md).

## Użycie na stronie

Skopiuj pliki z [`dist/`](dist/) obok strony:

```html
<link rel="stylesheet" href="kuropatwa.css">
<span class="kuropatwa">kosen, !ogä!! kornik.</span>
<span class="kuropatwa-drap">kosun.</span>
```

| Plik | Do czego |
|---|---|
| `kuropatwa.woff2`, `kuropatwa.woff` | zapis piórem, na stronę |
| `kuropatwa-drap.woff2`, `kuropatwa-drap.woff` | zapis pazurem, na stronę |
| `*.ttf` | instalacja w systemie (edytory, Foundry, grafika) |
| `kuropatwa.css` | gotowe `@font-face` i klasy `.kuropatwa`, `.kuropatwa-drap` |

**Wzornik z transliteratorem:** otwórz [`specimen/index.html`](specimen/index.html) w przeglądarce.
Wpisujesz tekst po łacinie i od razu widzisz go w Kuropatwie, razem z kluczem znaków.

## Zestaw znaków

Według dokumentu języka (rozdz. VI):

- litery `a–z`;
- polskie `ą ć ę ł ń ó ś ź ż`;
- `ä ö ü ß`;
- romańskie `á é í ó ú à è ì ò ù â ê î ô û ñ ã ç`;
- cyfry `0–9`;
- `. , : ; ! ? $ + - / =`.

Wielkie litery wskazują ten sam znak co małe.

## Budowanie

```bash
pip install -r requirements.txt
python3 tools/build.py      # fonty do dist/ + wzornik
python3 -m pytest -q        # testy
python3 tools/preview.py    # odświeża docs/preview.png
```

| Gdzie | Co |
|---|---|
| `src/kuropatwa/glyphs.py` | kształty znaków (szkielety kresek) i warstwy |
| `src/kuropatwa/render.py` | kreska pióra i pazura |
| `src/kuropatwa/build.py` | składanie fontu i CSS |
| `tools/specimen.py` | wzornik |
| `tests/` | zestaw znaków, rozróżnialność w 16/24 px, deterministyczność |

## Kto czego pilnuje

- **Język Birdfolk** (słowa, dźwięki, ortografia): czat/repo **Whitewood**. Tutaj tylko odczyt.
- **Pismo Kuropatwa** (kształty, font, lore pisma): **to repo**.
- Decyzje i postęp: [`docs/KAMIENIE.md`](docs/KAMIENIE.md).

## Rasy, które piszą Kuropatwą

Według taksonomii z dokumentu języka.

**Rdzenne (pierwszy krąg, `sekor`)**
- **Birdfolk:**
  - krukowate: Corvum, Kenku;
  - sowy: Strig, Owlin;
  - drapieżne: Raptor, Aarakocra;
  - naziemne: Gallus;
  - miejskie: Luma;
  - wodne: kaczkowate, mewowate.
- **Beastfolk:**
  - psowate: Vulpin, Lupin;
  - kotowate: Tabaxi, Leonin;
  - Loxodon;
  - Harengon;
  - Cervan;
  - Mapach;
  - Jerbeen;
  - jeżowate (Hedge);
  - łasicowate;
  - Ursine;
  - nietoperze.

**Wtórne (drugi krąg, `tekor`)**
- **Hybrids:** Minotaur, Centaur, Satyr.
- **Exotic:** Thri-kreen, Tortle.

## Prawa

Kształty liter, kod i fonty są własne. Humblescratch i pozostałe materiały Humblewood należą do
Hit Point Press. Ich licencja zabrania webfontu i rozpowszechniania, dlatego **nie ma ich w tym
repo**. Licencja publiczna Kuropatwy nie jest jeszcze wybrana.

## Uwaga o historii repozytorium

Na początku prac do repo przez pomyłkę trafił plik fontu Hit Point Press, przesłany jako materiał
referencyjny. Usunięto go, a historię gałęzi przepisano bez niego (26.11.2026). Repozytorium
zostanie przeniesione do nowego, czystego repo.
