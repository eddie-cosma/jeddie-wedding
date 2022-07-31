from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base, engine
from .helpers import random_id


class Guest(Base):
    __tablename__ = "guest"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    party_id = Column(Integer, ForeignKey("party.id"))
    party = relationship("Party", back_populates="guests")


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(6), nullable=False, default=random_id, unique=True, index=True)
    rsvp_responded = Column(Boolean, default=False)
    rsvp_plus_one_avail = Column(Integer, nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address")
    guests = relationship("Guest", back_populates="party")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    street_address = Column(String(100), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(30), nullable=True)
    postal_code = Column(String(10), nullable=False)
    country = Column(String(20), nullable=False)


Base.metadata.create_all(bind=engine)
