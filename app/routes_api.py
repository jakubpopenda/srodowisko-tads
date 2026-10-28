from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony, raporty_roku
from .validators import parametr_int
from .decorators import wymagany_parametr

api_bp = Blueprint("api", __name__)

@api_bp.get("/kpi")
def kpi():
    region = request.args.get("region")
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    dane = policz_wskazniki(sciezka, region)
    return jsonify(dane)

@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    raporty_lista = raporty_roku(rok)
    return jsonify(rok=rok, raporty=raporty_lista)