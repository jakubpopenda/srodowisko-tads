import csv

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

def zapisz_raport(rok, region):
    RAPORTY.append({"rok": int(rok), "region": region})

def raporty_roku(rok):
    return [r for r in RAPORTY if r["rok"] == int(rok)]

def zestawienie_regionow(sciezka):
    regiony = dostepne_regiony(sciezka)
    return [policz_wskazniki(sciezka, r) for r in sorted(regiony)]