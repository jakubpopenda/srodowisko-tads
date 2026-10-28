import logging
from flask import Flask
from .config import KONFIGURACJE
from .converters import RegionConverter

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)
    
    # Rejestracja własnego konwertera przed blueprintami
    app.url_map.converters["region"] = RegionConverter
    
    # Importy blueprintów muszą być wewnątrz funkcji, aby uniknąć zależności cyklicznej
    from .routes_api import api_bp
    from .routes_panel import panel_bp
    
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app