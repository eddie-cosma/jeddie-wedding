import json

from flask import render_template, Blueprint

from database import get_db
from database.model import Guest

bp = Blueprint('jeddie', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template("home.html")


@bp.route('/story')
def story():
    return render_template("story.html")


@bp.route('/wedding')
def wedding():
    return render_template("wedding.html")


@bp.route('/rsvp')
def rsvp():
    return render_template("rsvp.html")


@bp.route('/photos')
def photos():
    return render_template("photos.html")


@bp.route('/hotel')
def hotel():
    return render_template("hotel.html")


@bp.route('/registry')
def registry():
    return render_template("registry.html")


@bp.route('/test')
def test():
    session = get_db()
    values = session.query(Guest).all()
    results = [{'guest': value.email, 'party': value.party.name} for value in values]
    return json.dumps(results), 200, {'content_type': 'application/json'}
