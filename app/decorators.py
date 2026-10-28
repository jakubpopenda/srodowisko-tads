from functools import wraps
from flask import request, abort

def wymagany_parametr(nazwa):
    def dekorator(widok):
        @wraps(widok)
        def opakowanie(*args, **kwargs):
            if nazwa not in request.args:
                abort(400, description=f"Brak parametru {nazwa}")
            return widok(*args, **kwargs)
        return opakowanie
    return dekorator