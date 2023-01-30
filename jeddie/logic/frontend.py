import stripe
from flask import redirect, url_for, g, flash
from sqlalchemy.sql import func
from sqlalchemy.orm.scoping import scoped_session

from database.model import Item, Gift
from middleware.email import log_to_email

def is_item_available(session: scoped_session, item: Item) -> bool:
    total_purchased = session.query(Gift.item_id,
                                    func.coalesce(func.sum(Gift.quantity), 0).label('total')) \
        .filter_by(item_id=item.id).one_or_none()
    if item.max_quantity <= total_purchased.total:
        return False
    else:
        return True


def record_gift(session: scoped_session, item: Item, buyer: str, stripe_id: str | None = None):
    # Record the gift to log and email
    print(f'Gift of {"$%.2f" % (item.price / 100)} received from {buyer}')
    log_to_email(item, buyer, stripe_id)

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
    price = int(round(price, 2)) * 100
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
