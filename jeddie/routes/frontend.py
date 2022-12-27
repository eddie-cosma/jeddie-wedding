import json

from flask import g, current_app, render_template, Blueprint, abort, request, flash, redirect, url_for

from database import get_db
from database.model import Guest, Party, Meal, Item
from middleware.recaptcha import verify_recaptcha
from middleware.stripe import create_intent

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
    def prefix_lang_dict(translations: dict) -> dict:
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


@bp.route('/rsvp', methods=['GET', 'POST'])
@bp.route('/rsvp/<string:rsvp_code>', methods=['GET', 'POST'])
def rsvp(rsvp_code: str = None):
    recaptcha_site_key = current_app.config.get('RECAPTCHA_SITE_KEY', None)
    recaptcha_token = request.form.get('g-recaptcha-response', None)
    if request.method == 'GET' or not verify_recaptcha(recaptcha_token, request.remote_addr):
        return render_template('rsvp.html', rsvp_code=rsvp_code, site_key=recaptcha_site_key, **g.language)

    rsvp_code = rsvp_code or request.form.get('rsvp_code', '')
    rsvp_code = rsvp_code.upper()
    session = get_db()
    if party := session.query(Party).where(Party.code == rsvp_code).one_or_none():
        meals = session.query(Meal).all()
        return render_template("rsvp_detail.html", party=party, meals=meals, **g.language)
    else:
        flash(g.language.get('lang_invalid_rsvp_code'))
        return redirect(url_for('jeddie.rsvp'), 302)


@bp.route('/photos')
def photos():
    return render_template("photos.html", **g.language)


@bp.route('/hotel')
def hotel():
    return render_template("hotel.html", **g.language)


@bp.route('/registry')
def registry():
    return render_template("registry.html", **g.language)


@bp.route('/pay/<int:item_id>', methods=['GET'])
def pay(item_id: int):
    session = get_db()
    if item := session.query(Item).where(Item.id == item_id).one_or_none():
        stripe_key = current_app.config.get('STRIPE_API_KEY')
        intent = create_intent(amount=item.price)
        return render_template('pay.html', public_key=stripe_key, client_secret=intent.client_secret, **g.language)
    else:
        flash(g.language.get('lang_invalid_registry_item'))
        return redirect(url_for('jeddie.registry'), 302)

@bp.route('/post-pay', methods=['GET'])
def post_pay():
    stripe_key = current_app.config.get('STRIPE_API_KEY')
    return render_template('post-pay.html', public_key=stripe_key, **g.language)
