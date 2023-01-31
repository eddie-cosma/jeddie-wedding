from config import config
from database.model import Item


def create_intent(item: Item, email: str, buyer_name: str):
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.create(
        amount=item.price,
        currency='usd',
        description=item.name,
        automatic_payment_methods={'enabled': True},
        metadata={
            'buyer_name': buyer_name,
            'item_id': item.id,
        },
        receipt_email=email,
    )
    return intent


def get_intent_metadata(intent_id: str) -> dict:
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.retrieve(intent_id)
    return intent.metadata


def get_status(intent_id: str) -> str:
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.retrieve(intent_id)
    return intent.status
