import json

from flask import g, current_app, render_template, Blueprint, abort, request

from database import get_db
from database.model import Guest, Party

bp = Blueprint('jeddie', __name__, url_prefix='/<language_code>')


@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('language_code', g.language_code)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.language_code = values.pop('language_code', 'en')
    if g.language_code not in ['en', 'ro']:
        abort(404)

    # add 'lang_' prefix to every key in the json translation file
    def prefix_lang_dict(translations: dict):
        return {f'lang_{key}': value for (key, value) in translations.items()}

    language_file = f'{current_app.static_folder}/language/{g.language_code}.json'
    with open(language_file, 'r', encoding='utf8') as file:
        g.language = json.load(file, object_hook=prefix_lang_dict)


@bp.route('/')
def index():
    return render_template("home.html", **g.language)


@bp.route('/story')
def story():
    return render_template("story.html", **g.language)


@bp.route('/wedding')
def wedding():
    return render_template("wedding.html", **g.language)


@bp.route('/rsvp')
def rsvp():
    if request.method == 'GET':
        return render_template("rsvp.html", **g.language)


@bp.route('/rsvp/<string:rsvp_code>', methods=['GET', 'POST'])
def rsvp_detail(rsvp_code: str):
    session = get_db()
    party = session.query(Party).where(Party.code == rsvp_code).one_or_none()
    if not party:
        abort(404)
    elif request.method == 'GET':
        return render_template("rsvp_detail.html", party=party, **g.language)


@bp.route('/photos')
def photos():
    return render_template("photos.html", **g.language)


@bp.route('/hotel')
def hotel():
    return render_template("hotel.html", **g.language)


@bp.route('/registry')
def registry():
    return render_template("registry.html", **g.language)


@bp.route('/test')
def test():
    session = get_db()
    values = session.query(Guest).all()
    results = [{'guest': value.email, 'party': value.party.name} for value in values]
    return json.dumps(results), 200, {'content_type': 'application/json'}
