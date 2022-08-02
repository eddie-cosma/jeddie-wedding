from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from config import config

Base = declarative_base()
engine = create_engine(config.SQLALCHEMY_DB_STRING, echo=True, future=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    if 'db' not in g:
        # TODO: Separate create_all into initialization script
        from .model import Guest, Party, Address
        Base.metadata.create_all(bind=engine)
        g.db = session()

    return g.db
