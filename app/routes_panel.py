from datetime import date
from flask import Blueprint, request, abort, current_app, redirect, url_for, render_template, flash
from .services import policz_wskazniki, dostepne_regiony, raporty_roku, zapisz_raport, zestawienie_regionow
from werkzeug.utils import secure_filename
from .forms import FiltrForm, RaportForm, ZbiorForm
from .services import (
    policz_wskazniki,
    dostepne_regiony,
    raporty_roku,
    zapisz_raport,
    zestawienie_regionow,
    wykaz_raportow,
    wczytaj_zbior,
)
panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026

@panel_bp.get("/")
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = sorted(dostepne_regiony(sciezka))

    formularz = FiltrForm(request.args)
    formularz.region.choices = [("", "wszystkie")] + [(r, r) for r in regiony]

    region = rok = None
    if formularz.validate():
        region = formularz.region.data or None
        rok = formularz.rok.data
    else:
        flash("Kryteria zawężenia zostały pominięte", "ostrzezenie")

    w = policz_wskazniki(sciezka, region, rok)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])

    return render_template(
        "panel.html",
        formularz=formularz,
        wskazniki=w,
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today(),
    )
@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka)
    
    if kod not in regiony:
        abort(404, description=f"Nieznany region: {kod}")
        
    dane = policz_wskazniki(sciezka, kod)
    zestawienie = zestawienie_regionow(sciezka)
    return render_template("panel.html", wskazniki=dane, zestawienie=zestawienie, dzisiaj=date.today())

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    raporty = raporty_roku(rok)
    return render_template("report.html", rok=rok, zapisane=raporty)

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = sorted(dostepne_regiony(sciezka))
    istniejace = {(r["rok"], r["region"]) for r in wykaz_raportow()}

    formularz = RaportForm(istniejace=istniejace)
    formularz.region.choices = [(r, r) for r in regiony]

    if formularz.validate_on_submit():
        zapisz_raport(
            formularz.rok.data,
            formularz.region.data,
            formularz.uwagi.data or "",
        )
        flash(f"Raport za rok {formularz.rok.data} zapisany", "sukces")
        return redirect(url_for("panel.raport", rok=formularz.rok.data), 303)

    status = 422 if formularz.errors else 200
    return render_template("new_report.html", formularz=formularz), status

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)

@panel_bp.route("/wczytaj", methods=["GET", "POST"])
def wczytaj():
    formularz = ZbiorForm()
    if formularz.validate_on_submit():
        plik = formularz.plik.data
        nazwa = secure_filename(plik.filename)
        try:
            liczba = wczytaj_zbior(plik.stream)
        except ValueError as blad:
            formularz.plik.errors.append(f"Niepoprawna zawartość: {blad}")
        else:
            flash(f"Wczytano {liczba} zamówień z pliku {nazwa}", "sukces")
            return redirect(url_for("panel.wczytaj"), 303)

    status = 422 if formularz.errors else 200
    return render_template("upload.html", formularz=formularz), status