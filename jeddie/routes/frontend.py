import json

from flask import render_template, Blueprint

from database import get_db
from database.model import Guest

bp = Blueprint('simple_page', __name__, url_prefix='/')


@bp.route('/')
def hello():
    return render_template("base.html", title="Home")


@bp.route('/test')
def test():
    session = get_db()
    values = session.query(Guest).all()
    results = [{'guest': value.email, 'party': value.party.name} for value in values]
    return json.dumps(results), 200, {'content_type': 'application/json'}
