from flask import redirect, url_for, g, flash
from sqlalchemy.sql import func
from sqlalchemy.orm.scoping import scoped_session

from database.model import Item, Gift


def is_item_available(session: scoped_session, item: Item) -> bool:
    total_purchased = session.query(Gift.item_id,
                                    func.coalesce(func.sum(Gift.quantity), 0).label('total')) \
        .filter_by(item_id=item.id).one_or_none()
    if item.max_quantity <= total_purchased.total:
        return False
    else:
        return True


def record_gift(session: scoped_session, item: Item, buyer: str):
    price_format = g.language.get('lang_registry_price_format', '$%.2f')

    # Record the gift to log and email
    print(f'Gift of {price_format % (item.price / 100)} received from {buyer}')
    # TODO : Record email

    # Record the gift to database
    gift = Gift(buyer_name=buyer, item_id=item.id, quantity=1)
    session.add(gift)
    session.commit()
    print(f'\tGift id: {gift.id}')

    # Thank the buyer
    flash(f'Your cash/check gift of {price_format % (item.price / 100)} has been recorded. Thank you, {buyer}.')


def create_custom_gift(session: scoped_session, price: float):
    name = 'Custom gift'
    price = int(round(price, 2))
    custom_item = Item(
        name=name,
        name_ro=name,
        price=price * 100,
        max_quantity=1,
        public=False,
    )
    session.add(custom_item)
    session.commit()

    return custom_item
