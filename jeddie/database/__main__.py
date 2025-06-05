"""
Database initialization script.

This script is used to initialize the database schema. It creates all necessary
tables if they don't exist. For SQLite databases, it also ensures the database
file exists before attempting to create the schema.
"""

from pathlib import Path

from config import config
from . import Base, engine
from .model import Guest, Party, Item, Gift

# For SQLite databases, ensure the database file exists
if config.DB_TYPE == "SQLITE":
    database_file = Path(config.SQLALCHEMY_DB_STRING.split(':', 1)[1])
    if not database_file.exists():
        database_file.touch()

# Create all tables defined in the models
Base.metadata.create_all(bind=engine)
