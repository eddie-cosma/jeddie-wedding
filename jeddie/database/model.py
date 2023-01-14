from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from . import Base
from .helpers import random_id


class Guest(Base):
    __tablename__ = 'guest'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=True)
    party_id = Column(Integer, ForeignKey('party.id'))
    party = relationship('Party', back_populates='guests')
    meal_id = Column(Integer, ForeignKey('meal.id'))
    meal = relationship('Meal')
    dietary_restriction = Column(String(140), nullable=True)


class Party(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(6), nullable=False, default=random_id, unique=True, index=True)
    rsvp_responded = Column(Boolean, default=False)
    total_guests_allowed = Column(Integer, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address')
    guests = relationship('Guest', back_populates='party')


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_address = Column(String(100), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(30), nullable=True)
    postal_code = Column(String(10), nullable=False)
    country = Column(String(20), nullable=False)


class Meal(Base):
    __tablename__ = 'meal'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    vegan = Column(Boolean, nullable=False, default=False)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_ro = Column(String(100), nullable=False)
    description = Column(String(280), nullable=True)
    description_ro = Column(String(280), nullable=True)
    photo_filename = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    max_quantity = Column(Integer, nullable=False)


class Gift(Base):
    __tablename__ = 'gift'
    id = Column(Integer, primary_key=True)
    buyer_name = Column(String(100), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship("Item")
    quantity = Column(Integer, nullable=False, default=1)

