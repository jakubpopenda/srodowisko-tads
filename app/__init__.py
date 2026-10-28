import logging
import time
from flask import Flask, g
from .config import KONFIGURACJE
from .converters import RegionConverter
from .errors import zarejestruj_obsluge_bledow

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)
    
    app.url_map.converters["region"] = RegionConverter
    
    @app.before_request
    def przed_zadaniem():
        g.start_time = time.perf_counter()
        
    @app.after_request
    def po_zadaniu(odpowiedz):
        if hasattr(g, "start_time"):
            czas = (time.perf_counter() - g.start_time) * 1000
            odpowiedz.headers["X-Czas-Ms"] = f"{czas:.2f}"
        return odpowiedz

    zarejestruj_obsluge_bledow(app)
    
    from .routes_api import api_bp
    from .routes_panel import panel_bp
    
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")
    
    return app