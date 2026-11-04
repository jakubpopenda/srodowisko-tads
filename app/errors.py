from flask import request, jsonify, render_template
from werkzeug.exceptions import HTTPException

def zarejestruj_obsluge_bledow(app):
    @app.errorhandler(HTTPException)
    def obsluz_blad(e):
        if request.path.startswith("/api"):
            return jsonify(blad=e.description, kod=e.code), e.code
        return render_template("errors/error.html", kod=e.code, opis=e.description), e.code