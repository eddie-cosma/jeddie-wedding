from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Session

from . import Base
from .helpers import generate_uuid


class Guest(Base):
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
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uuid = Column(String, nullable=False, default=generate_uuid)
    guests = relationship('Guest', back_populates='party')

    def get_next_unfinalized_guest(self) -> Guest | None:
        session = Session.object_session(self)
        return session.query(Guest).where(Guest.party == self,
                                          Guest.attending == True,
                                          Guest.finalized == False).first()


class Meal(Base):
    __tablename__ = 'meal'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_ro = Column(String(100), nullable=False)
    vegan = Column(Boolean, nullable=False, default=False)


class Item(Base):
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
    __tablename__ = 'gift'
    id = Column(Integer, primary_key=True)
    stripe_id = Column(String(100), nullable=True, index=True, unique=True)
    buyer_name = Column(String(100), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship("Item")
    quantity = Column(Integer, nullable=False, default=1)

