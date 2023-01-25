from config import config
from database.model import Item


def create_intent(item: Item, email: str):
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.create(
        amount=item.price,
        currency='usd',
        description=item.name,
        automatic_payment_methods={'enabled': True},
        receipt_email=email,
    )
    return intent
