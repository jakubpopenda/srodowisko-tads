from flask import Flask, request, abort, jsonify
from services import policz_wskazniki, dostepne_regiony

app = Flask(__name__)

@app.get("/")
def index():
    return "Panel wskaźników"

@app.get("/kpi")
def kpi_html():
    region = request.args.get("region")
    regiony = dostepne_regiony("dane/zamowienia.csv")
    
    # Dodane sprawdzenie: przerywamy tylko gdy region został podany, ale jest nieznany
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    dane = policz_wskazniki("dane/zamowienia.csv", region)
    tekst_region = region if region else "Całość"
    return f"<h1>Wskaźniki: {tekst_region}</h1><p>Marża: {dane['marza']:.2%}</p>"

@app.get("/api/kpi")
def kpi_json():
    region = request.args.get("region")
    regiony = dostepne_regiony("dane/zamowienia.csv")
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    dane = policz_wskazniki("dane/zamowienia.csv", region)
    return jsonify(dane)