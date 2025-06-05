"""
Stripe transaction refresh tool.

This script is designed to be run as a cron job to manage pending Stripe transactions
and keep gift quantities in sync with payment status. It performs the following tasks:

1. Finds all gifts with quantity 0 (pending payment)
2. For each gift with a Stripe payment intent:
   - If payment is confirmed, updates quantity to 1
   - If payment is pending and older than 24 hours, cancels the intent
3. Commits all changes to the database

This tool is necessary because gift quantities are initially set to 0 when a payment
intent is created, to prevent the available quantity from decrementing until payment
is confirmed. This script ensures that confirmed payments are properly reflected in
the gift registry.
"""

import time

import stripe

from config import config
from database import session
from database.model import Gift

stripe.api_key = config.STRIPE_SECRET

# Calculate timestamp for 24 hours ago
DAY_OLD_TIME = int(time.time()) - 86400

# Find all gifts with pending payment (quantity = 0)
gifts = session.query(Gift).where(Gift.quantity == 0).all()

for gift in gifts:
    if gift.stripe_id.startswith('pi_'):
        # Retrieve payment intent status from Stripe
        intent = stripe.PaymentIntent.retrieve(gift.stripe_id)
        
        if intent.status == 'succeeded':
            # Payment confirmed, update quantity
            gift.quantity = 1
            print(f'Updated gift {gift.stripe_id} quantity to 1.')
        elif intent.status.startswith('requires_') and intent.created < DAY_OLD_TIME:
            # Payment abandoned, cancel intent
            intent.cancel(cancellation_reason='abandoned')
            gift.stripe_id = f'CANCELLED_{gift.stripe_id}'
            print(f'Cancelled payment intent for gift {gift.stripe_id}.')

session.commit()
