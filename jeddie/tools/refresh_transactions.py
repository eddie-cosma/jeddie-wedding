import time

import stripe

from config import config
from database import session
from database.model import Gift

stripe.api_key = config.STRIPE_SECRET
DAY_OLD_TIME = int(time.time()) - 86400

gifts = session.query(Gift).where(Gift.quantity == 0).all()
for gift in gifts:
    if gift.stripe_id.startswith('pi_'):
        intent = stripe.PaymentIntent.retrieve(gift.stripe_id)
        if intent.status == 'succeeded':
            gift.quantity = 1
            print(f'Updated gift {gift.stripe_id} quantity to 1.')
        elif intent.status.startswith('requires_') and intent.created < DAY_OLD_TIME:
            intent.cancel(cancellation_reason='abandoned')
            gift.stripe_id = f'CANCELLED_{gift.stripe_id}'
            print(f'Cancelled payment intent for gift {gift.stripe_id}.')
session.commit()
