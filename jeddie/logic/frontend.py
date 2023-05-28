from decimal import Decimal

import stripe
from flask import redirect, url_for, g, flash
from sqlalchemy.sql import func
from sqlalchemy.orm.scoping import scoped_session

from database import get_db
from database.model import Item, Gift, Guest, Party
from exceptions.exceptions import InvalidRSVPException
from middleware.email import log_to_email


class GuestRSVP:
    def __init__(self, party: Party, guest_id: str | int):
        self._session = get_db()
        self.party = party
        self.guest = guest_id

    @property
    def guest(self) -> Guest:
        return self._guest

    @guest.setter
    def guest(self, guest_id: str | int):
        try:
            guest_id = int(guest_id)
        except ValueError:
            raise InvalidRSVPException
        self._guest = self._session.query(Guest).where(Guest.id == guest_id).one_or_none()

        if not self._guest or not self._guest_in_party():
            raise InvalidRSVPException

    def respond_to_rsvp(self, attending_yn: str):
        try:
            attending_yn = bool(int(attending_yn))
        except ValueError:
            raise InvalidRSVPException
        self.guest.attending = attending_yn
        self.guest.finalized = not attending_yn
        self._session.commit()

    def set_rsvp_details(self, first_name: str | None, last_name: str | None, meal_id: int | None,
                         dietary_restriction: str | None, song_choice: str | None):
        if self.guest.is_plus_one:
            if not first_name or not last_name:
                raise InvalidRSVPException('lang_rsvp_missing_name')

            self.guest.first_name = first_name[0:30]
            self.guest.last_name = last_name[0:30]

        if not meal_id:
            raise InvalidRSVPException('lang_rsvp_missing_meal')

        self.guest.meal_id = meal_id
        if dietary_restriction:
            self.guest.dietary_restriction = dietary_restriction[0:140]
        if song_choice:
            self.guest.song_choice = song_choice[0:100]
        self.guest.finalized = True
        self._session.commit()

    def _guest_in_party(self):
        return self.guest in self.party.guests


def get_name_matches(session: scoped_session, search_term: str) -> list[Guest] | None:
    *first_names, last_name = search_term.split(' ')
    first_name = ' '.join(first_names)

    hits = session.query(Party).filter(
            Party.guests.any(func.lower(Guest.last_name) == last_name.lower())
    ).distinct().all()
    for hit in hits:
        if first_name in [guest.first_name for guest in hit.guests]:
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


def create_custom_gift(session: scoped_session, price: Decimal):
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
