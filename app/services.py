import csv
import io
def wczytaj_zamowienia(sciezka):
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        return list(csv.DictReader(plik))

def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    return sorted(list(set(wiersz['region'] for wiersz in zamowienia)))

def policz_wskazniki(sciezka, region=None, rok=None):
    wiersze = wczytaj_zamowienia(sciezka)  # lub Twoja dotychczasowa funkcja odczytu CSV
    if region:
        wiersze = [z for z in wiersze if z["region"] == region]
    if rok is not None:
        wiersze = [z for z in wiersze if z["data"].startswith(str(rok))]

    przychod = sum(float(z["przychod"]) for z in wiersze)
    koszt = sum(float(z["koszt"]) for z in wiersze)
    marza = round((przychod - koszt) / przychod, 4) if przychod else 0.0

    return {
        "region": region or "wszystkie",
        "przychod": przychod,
        "koszt": koszt,
        "marza": marza,
        "liczba_zamowien": len(wiersze),
    }
RAPORTY = []
_RAPORTY = []


def zapisz_raport(rok, region, uwagi=""):
    _RAPORTY.append({"rok": rok, "region": region, "uwagi": uwagi})


def raporty_roku(rok):
    return [r for r in _RAPORTY if r["rok"] == rok]


def wykaz_raportow():
    return list(_RAPORTY)

def zestawienie_regionow(sciezka):
    regiony = dostepne_regiony(sciezka)
    return [policz_wskazniki(sciezka, r) for r in sorted(regiony)]

def wczytaj_zbior(strumien):
    tekst = strumien.read().decode("utf-8")
    czytnik = csv.DictReader(io.StringIO(tekst))
    naglowek = set(czytnik.fieldnames or [])
    wymagane = {"data", "region", "przychod", "koszt"}
    brakujace = sorted(wymagane - naglowek)
    if brakujace:
        raise ValueError(f"brak kolumn: {', '.join(brakujace)}")
    return sum(1 for _ in czytnik)