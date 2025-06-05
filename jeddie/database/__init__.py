"""
Database initialization and session management.

This module handles the setup of SQLAlchemy database connection and session management.
It provides a function to get a database session from the Flask application context.
"""

import sys

from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from config import config

Base = declarative_base()

# Use SQLite for testing, configured database for production
if 'pytest' in sys.modules:
    connection_string = "sqlite://"
else:
    connection_string = config.SQLALCHEMY_DB_STRING

# Create database engine and session factory
engine = create_engine(connection_string, echo=True, future=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    """
    Get a database session from the Flask application context.
    
    Returns:
        Session: A SQLAlchemy database session
    """
    if 'db' not in g:
        from .model import Guest, Party
        g.db = session()

    return g.db
