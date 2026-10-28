from flask import Blueprint, request, abort, current_app
from .services import policz_wskazniki, dostepne_regiony, raporty_roku

panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026

@panel_bp.get("/")
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi():
    region = request.args.get("region")
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    dane = policz_wskazniki(sciezka, region)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", dane["region"])
    
    tekst_region = region if region else "Całość"
    return f"<h1>Wskaźniki: {tekst_region}</h1><p>Marża: {dane['marza']:.2%}</p>"

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka)
    
    if kod not in regiony:
        abort(404, description=f"Nieznany region: {kod}")
        
    dane = policz_wskazniki(sciezka, kod)
    return f"<h1>Region {kod}</h1><p>Zamówień: {dane['liczba_zamowien']}</p>"

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    raporty = raporty_roku(rok)
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {len(raporty)}</p>"