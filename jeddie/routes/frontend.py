import json

from flask import g, current_app, render_template, Blueprint, abort, request, flash, redirect, url_for
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from database import get_db
from database.model import Guest, Party, Meal, Item, Gift
from logic.frontend import is_item_available, record_gift, create_custom_gift
from middleware.recaptcha import verify_recaptcha
from middleware.stripe import create_intent, get_intent_metadata

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
    session = get_db()
    sq = session.query(Gift.item_id, func.sum(Gift.quantity).label('total_purchased'))\
                .group_by(Gift.item_id)\
                .subquery()
    counts = aliased(Gift, sq, 'purchases')
    items = session.query(Item, (Item.max_quantity - func.coalesce(sq.c.total_purchased, 0)).label('remaining'))\
                   .join(counts, counts.item_id == Item.id, isouter=True)
    return render_template("registry.html", items=items, **g.language)


@bp.route('/registry/custom', methods=['GET', 'POST'])
def registry_custom():
    if request.method == 'POST':
        session = get_db()
        price = request.form.get('price', 0)
        if price.isnumeric() and 5000 > float(price) > 1:
            item = create_custom_gift(session, float(price))
            return redirect(url_for('jeddie.pay', item_id=item.id), 302)
        else:
            flash('You must enter a dollar amount between $1 and $5000 for custom gifts. For gifts exceeding this'
                  ' amount, please consider leaving a check at the card box.')
            return redirect(url_for('jeddie.registry_custom'), 302)

    return render_template("registry-custom.html", **g.language)


@bp.route('/promise/<int:item_id>', methods=['GET', 'POST'])
def promise(item_id: int):
    session = get_db()
    if item := session.query(Item).where(Item.id == item_id).one_or_none():
        if not is_item_available(session, item):
            return redirect(url_for('jeddie.registry'), 302)

        if request.method == 'GET':
            return render_template('promise.html', item=item, **g.language)
        else:
            buyer = request.form.get('buyer_name', None)
            if not buyer:
                flash('Please enter a valid name.')
                return render_template('promise.html', item=item, **g.language)

            record_gift(session, item, buyer)
            price_format = g.language.get('lang_registry_price_format', '$%.2f')
            flash(f'Your cash/check gift of {price_format % (item.price / 100)} has been recorded. Thank you, {buyer}.')
            return redirect(url_for('jeddie.registry'), 302)

    flash(g.language.get('lang_invalid_registry_item'))
    return redirect(url_for('jeddie.registry'), 302)


@bp.route('/pay/<int:item_id>', methods=['GET', 'POST'])
def pay(item_id: int):
    session = get_db()
    if item := session.query(Item).where(Item.id == item_id).one_or_none():
        if not is_item_available(session, item):
            return redirect(url_for('jeddie.registry'), 302)

        if request.method == 'POST':
            # Initialize payment process
            email = request.form.get('email', None)
            buyer_name = request.form.get('name', None)
            if not email or not buyer_name:
                flash('Please enter a valid name and email address.')
                return render_template('pre-pay.html', item=item, **g.language)

            stripe_key = current_app.config.get('STRIPE_API_KEY')
            intent = create_intent(item=item, email=email, buyer_name=buyer_name)
            return render_template('pay.html', item=item, public_key=stripe_key, intent=intent, **g.language)
        else:
            return render_template('pre-pay.html', item=item, **g.language)

    flash(g.language.get('lang_invalid_registry_item'))
    return redirect(url_for('jeddie.registry'), 302)


@bp.route('/post-pay', methods=['GET'])
def post_pay():
    stripe_key = current_app.config.get('STRIPE_API_KEY')
    intent = request.args.get('payment_intent', None)
    client_secret = request.args.get('payment_intent', None)
    if not intent or not client_secret:
        flash('Something went wrong.')
        return redirect(url_for('jeddie.registry'), 302)

    metadata = get_intent_metadata(intent)
    if 'item_id' not in metadata.keys() or 'buyer_name' not in metadata.keys():
        flash('Something went wrong.')
        return redirect(url_for('jeddie.registry'), 302)

    session = get_db()
    if session.query(Gift).where(Gift.stripe_id == intent).count() == 0:
        item = session.query(Item).where(Item.id == metadata['item_id']).one_or_none()
        record_gift(session, item, metadata['buyer_name'], intent)

    return render_template('post-pay.html', public_key=stripe_key, **g.language)
