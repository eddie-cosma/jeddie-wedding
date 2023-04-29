import sys

from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from config import config

Base = declarative_base()

if 'pytest' in sys.modules:
    connection_string = "sqlite://"
else:
    connection_string = config.SQLALCHEMY_DB_STRING

engine = create_engine(connection_string, echo=True, future=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    if 'db' not in g:
        from .model import Guest, Party
        g.db = session()

    return g.db
