from config import config


def create_intent(amount: int):
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        automatic_payment_methods={'enabled': True},
    )
    return intent
