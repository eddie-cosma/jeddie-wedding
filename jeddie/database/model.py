from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine


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
