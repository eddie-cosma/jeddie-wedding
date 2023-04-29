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
def rsvp():
    recaptcha_site_key = current_app.config.get('RECAPTCHA_SITE_KEY', None)
    recaptcha_token = request.form.get('g-recaptcha-response', None)
    if request.method == 'GET':
        return render_template('rsvp.html', site_key=recaptcha_site_key, **g.language)
    elif request.method == 'POST':
        if not verify_recaptcha(recaptcha_token, request.remote_addr):
            flash(g.language.get('lang_invalid_captcha_code'))
            return render_template('rsvp.html', site_key=recaptcha_site_key, **g.language)
        # TODO: Write rest of logic for form submission

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

        try:
            price = float(price)
            price_is_numeric = True
        except ValueError:
            price_is_numeric = False

        if price_is_numeric and 5000 >= price >= 1:
            item = create_custom_gift(session, price)
            return redirect(url_for('jeddie.pay', item_id=item.id), 302)
        else:
            flash(g.language.get('lang_error_invalid_gift_amount'))
            return render_template("registry-custom.html", **g.language)

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
                flash(g.language.get('lang_error_enter_valid_name'))
                return render_template('promise.html', item=item, **g.language)

            record_gift(session, item, buyer)
            price_format = g.language.get('lang_registry_price_format', '$%.2f')
            price_string = price_format % (item.price / 100)
            success_message_parts = (g.language.get('lang_success_gift_recorded_1'), price_string,
                                     g.language.get('lang_success_gift_recorded_2'), buyer, '.')
            flash(''.join(success_message_parts))
            return redirect(url_for('jeddie.registry'), 302)

    flash(g.language.get('lang_invalid_registry_item'))
    return redirect(url_for('jeddie.registry'), 302)


@bp.route('/pay/<int:item_id>', methods=['GET', 'POST'])
def pay(item_id: int):
    session = get_db()
    if item := session.query(Item).where(Item.id == item_id).one_or_none():
        if not is_item_available(session, item):
            return redirect(url_for('jeddie.registry'), 302)

        recaptcha_site_key = current_app.config.get('RECAPTCHA_SITE_KEY', None)
        recaptcha_token = request.form.get('g-recaptcha-response', None)

        if request.method == 'POST' and verify_recaptcha(recaptcha_token, request.remote_addr):
            # Initialize payment process
            email = request.form.get('email', None)
            buyer_name = request.form.get('name', None)
            if not email or not buyer_name:
                flash(g.language.get('lang_error_enter_valid_name_email'))
                return render_template('pre-pay.html', item=item, site_key=recaptcha_site_key, **g.language)

            stripe_key = current_app.config.get('STRIPE_API_KEY')
            try:
                intent = create_intent(item=item, email=email, buyer_name=buyer_name)
            except:
                flash(g.language.get('lang_error_enter_valid_email'))
                return render_template('pre-pay.html', item=item, site_key=recaptcha_site_key, **g.language)

            return render_template('pay.html', item=item, public_key=stripe_key, intent=intent, **g.language)
        else:
            return render_template('pre-pay.html', item=item, site_key=recaptcha_site_key, **g.language)

    flash(g.language.get('lang_invalid_registry_item'))
    return redirect(url_for('jeddie.registry'), 302)


@bp.route('/post-pay', methods=['GET'])
def post_pay():
    stripe_key = current_app.config.get('STRIPE_API_KEY')
    intent = request.args.get('payment_intent', None)
    client_secret = request.args.get('payment_intent', None)
    if not intent or not client_secret:
        flash(g.language.get('lang_error_something_went_wrong'))
        return redirect(url_for('jeddie.registry'), 302)

    metadata = get_intent_metadata(intent)
    if 'item_id' not in metadata.keys() or 'buyer_name' not in metadata.keys():
        flash(g.language.get('lang_error_something_went_wrong'))
        return redirect(url_for('jeddie.registry'), 302)

    session = get_db()
    if session.query(Gift).where(Gift.stripe_id == intent).count() == 0:
        item = session.query(Item).where(Item.id == metadata['item_id']).one_or_none()
        record_gift(session, item, metadata['buyer_name'], intent)

    return render_template('post-pay.html', public_key=stripe_key, **g.language)
