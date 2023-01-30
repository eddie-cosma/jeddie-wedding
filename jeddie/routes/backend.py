import json

from flask import Blueprint, make_response

from database import get_db
from database.model import Gift
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
