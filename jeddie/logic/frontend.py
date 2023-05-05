import stripe
from flask import redirect, url_for, g, flash
from sqlalchemy.sql import func
from sqlalchemy.orm.scoping import scoped_session

from database.model import Item, Gift, Guest
from middleware.email import log_to_email


def get_name_matches(session: scoped_session, search_term: str) -> list[Guest] | None:
    *first_names, last_name = search_term.split(' ')
    first_name = ' '.join(first_names)

    hits = session.query(Guest).where(Guest.last_name == last_name).all()
    for hit in hits:
        if hit.first_name == first_name:
            return [hit]
    else:
        return hits


def is_item_available(session: scoped_session, item: Item) -> bool:
    total_purchased = session.query(func.coalesce(func.sum(Gift.quantity), 0).label('total')) \
                             .filter_by(item_id=item.id).one_or_none()
    if item.max_quantity <= total_purchased.total:
        return False
    else:
        return True


def record_gift(session: scoped_session, item: Item, buyer: str, stripe_id: str = None):
    # Record the gift to log and email
    print(f'Gift of {"$%.2f" % (item.price / 100)} received from {buyer}')

    # Set quantity = 0 if it's a Stripe transaction until we can confirm payment with async process
    if stripe_id:
        quantity = 0
    else:
        quantity = 1

    # Record the gift to database
    gift = Gift(buyer_name=buyer, item_id=item.id, quantity=quantity, stripe_id=stripe_id)
    session.add(gift)
    session.commit()
    print(f'\tGift id: {gift.id}')


def create_custom_gift(session: scoped_session, price: float):
    name = 'Custom gift'
    price = int(round(price, 2) * 100)
    custom_item = Item(
        name=name,
        name_ro=name,
        price=price,
        max_quantity=1,
        public=False,
    )
    session.add(custom_item)
    session.commit()

    return custom_item
