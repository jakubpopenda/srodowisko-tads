from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony

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