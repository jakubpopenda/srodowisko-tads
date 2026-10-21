from flask import Blueprint, request, abort, current_app
from .services import policz_wskazniki, dostepne_regiony

panel_bp = Blueprint("panel", __name__)

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