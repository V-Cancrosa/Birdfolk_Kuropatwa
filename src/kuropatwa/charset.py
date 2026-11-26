"""Zestaw znaków Kuropatwy wg dokumentu języka (rozdz. VI)."""

BASIC = "abcdefghijklmnopqrstuvwxyz"
POLISH = "ąćęłńóśźż"
GERMAN = "äöüß"
ROMANCE = "áéíóúàèìòùâêîôûñãç"
DIGITS = "0123456789"
PUNCT = ".,:;!?"
OTHER = "$+-/="

# kolejność zachowana, bez powtórzeń (ó występuje w dwóch grupach)
REQUIRED = "".join(dict.fromkeys(BASIC + POLISH + GERMAN + ROMANCE + DIGITS + PUNCT + OTHER))

LAYERS = ("core", "mammal", "nasal", "loxodon", "imperial", "punct", "digit")
