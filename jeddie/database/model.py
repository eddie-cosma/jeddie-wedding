"""
Database models for the wedding website.

This module defines the SQLAlchemy models for the wedding website database,
including guest management, party organization, meal selection, and gift registry.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Session

from . import Base
from .helpers import generate_uuid


class Guest(Base):
    """
    Model representing a wedding guest.
    
    Attributes:
        id (int): Primary key
        first_name (str): Guest's first name
        last_name (str): Guest's last name
        attending (bool): Whether the guest is attending
        party_id (int): Foreign key to the guest's party
        party (Party): Relationship to the guest's party
        meal_id (int): Foreign key to the guest's meal choice
        meal (Meal): Relationship to the guest's meal choice
        dietary_restriction (str): Any dietary restrictions
        song_choice (str): Guest's song request
        is_plus_one (bool): Whether the guest is a plus-one
        finalized (bool): Whether the guest's RSVP is finalized
    """
    __tablename__ = 'guest'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    attending = Column(Boolean, nullable=True)
    party_id = Column(Integer, ForeignKey('party.id'))
    party = relationship('Party', back_populates='guests')
    meal_id = Column(Integer, ForeignKey('meal.id'))
    meal = relationship('Meal')
    dietary_restriction = Column(String(140), nullable=True)
    song_choice = Column(String(100), nullable=True)
    is_plus_one = Column(Boolean, nullable=False, default=False)
    finalized = Column(Boolean, nullable=False, default=False)


class Party(Base):
    """
    Model representing a group of guests.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the party
        uuid (str): Unique identifier for the party
        guests (list[Guest]): List of guests in the party
        
    Methods:
        get_next_unfinalized_guest: Returns the next guest in the party that needs to finalize their RSVP
    """
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uuid = Column(String, nullable=False, default=generate_uuid)
    guests = relationship('Guest', back_populates='party')

    def get_next_unfinalized_guest(self) -> Guest | None:
        """
        Get the next guest in the party that needs to finalize their RSVP.
        
        Returns:
            Guest | None: The next unfinalized guest, or None if all guests are finalized
        """
        session = Session.object_session(self)
        return session.query(Guest).where(Guest.party == self,
                                          Guest.attending == True,
                                          Guest.finalized == False).first()


class Meal(Base):
    """
    Model representing a meal option.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the meal in English
        name_ro (str): Name of the meal in Romanian
        vegan (bool): Whether the meal is vegan
    """
    __tablename__ = 'meal'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_ro = Column(String(100), nullable=False)
    vegan = Column(Boolean, nullable=False, default=False)


class Item(Base):
    """
    Model representing a gift registry item.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the item in English
        name_ro (str): Name of the item in Romanian
        description (str): Description of the item in English
        description_ro (str): Description of the item in Romanian
        photo_filename (str): Filename of the item's photo
        price (int): Price of the item in cents
        max_quantity (int): Maximum quantity available
        public (bool): Whether the item is publicly visible
    """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_ro = Column(String(100), nullable=False)
    description = Column(String(280), nullable=True)
    description_ro = Column(String(280), nullable=True)
    photo_filename = Column(String(100), nullable=True)
    price = Column(Integer, nullable=False)
    max_quantity = Column(Integer, nullable=False, default=1)
    public = Column(Boolean, nullable=False, default=False)


class Gift(Base):
    """
    Model representing a gift purchase.
    
    Attributes:
        id (int): Primary key
        stripe_id (str): Stripe payment intent ID
        buyer_name (str): Name of the gift buyer
        item_id (int): Foreign key to the purchased item
        item (Item): Relationship to the purchased item
        quantity (int): Quantity of the item purchased
    """
    __tablename__ = 'gift'
    id = Column(Integer, primary_key=True)
    stripe_id = Column(String(100), nullable=True, index=True, unique=True)
    buyer_name = Column(String(100), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship("Item")
    quantity = Column(Integer, nullable=False, default=1)

