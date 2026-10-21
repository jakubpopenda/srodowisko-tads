import csv

def wczytaj_zamowienia(sciezka):
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        return list(csv.DictReader(plik))

def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    return sorted(list(set(wiersz['region'] for wiersz in zamowienia)))

def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    
    if region is not None:
        zamowienia = [w for w in zamowienia if w['region'] == region]
        
    liczba_zamowien = len(zamowienia)
    przychod = sum(float(w['przychod']) for w in zamowienia)
    koszt = sum(float(w['koszt']) for w in zamowienia)
    
    if przychod == 0:
        marza = 0.0
    else:
        marza = round((przychod - koszt) / przychod, 4)
        
    return {
        'region': region,
        'liczba_zamowien': liczba_zamowien,
        'przychod': przychod,
        'koszt': koszt,
        'marza': marza
    }