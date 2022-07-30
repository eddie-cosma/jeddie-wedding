import json

from flask import render_template, Blueprint

from .database import Session
from .database.model import Guest

frontend_guest = Blueprint('simple_page', __name__, url_prefix='/')


@frontend_guest.route('/')
def hello():
    return render_template("base.html", title="Home")


@frontend_guest.route('/test')
def test():
    values = Session.query(Guest).all()
    results = [{'guest': value.email} for value in values]
    return json.dumps(results), 200, {'content_type': 'application/json'}
