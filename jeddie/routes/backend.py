import socket

from flask import Blueprint, make_response, render_template, request, abort

from database import get_db
from database.model import Gift, Guest
from middleware.stripe import get_status

bp = Blueprint('jeddie_backend', __name__)


@bp.route('/refresh_stripe_qty/<string:payment_intent>', methods=['GET'])
def refresh_stripe_qty(payment_intent: str):
    session = get_db()
    if gift := session.query(Gift).where(Gift.stripe_id == payment_intent).one_or_none():
        if get_status(payment_intent) == 'succeeded' and gift.quantity == 0:
            gift.quantity = 1
            session.commit()
            return make_response('Gift updated', 200)
        else:
            return make_response('Gift not updated', 200)

    return make_response('Gift not found', 404)


@bp.route('/rsvp_responses', methods=['GET'])
def rsvp_responses():
    if request.remote_addr != socket.gethostbyname('vpn.eddiecosma.com'):
        return abort(404)

    session = get_db()
    guests = session.query(Guest).all()
    if 'csv' in request.args.keys():
        return render_template('rsvp-list.csv', guests=guests), 200, {'Content-Type': 'text/csv; charset=utf-8'}
    else:
        return render_template('rsvp-list.html', guests=guests)
