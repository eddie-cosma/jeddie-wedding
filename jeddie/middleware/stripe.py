"""
Stripe payment intent middleware.

This module provides functions to create and retrieve payment intents from Stripe.
"""

from config import config
from database.model import Item


def create_intent(item: Item, email: str, buyer_name: str):
    """
    Create a payment intent for a given item.
    
    Args:
        item: The item to create a payment intent for
        email: The email of the buyer
    """
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
    """
    Get the metadata for a given payment intent.
    
    Args:
        intent_id: The ID of the payment intent
    """
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.retrieve(intent_id)
    return intent.metadata


def get_status(intent_id: str) -> str:
    """
    Get the status of a given payment intent.
    
    Args:
        intent_id: The ID of the payment intent
    """
    import stripe
    stripe.api_key = config.STRIPE_SECRET
    intent = stripe.PaymentIntent.retrieve(intent_id)
    return intent.status
