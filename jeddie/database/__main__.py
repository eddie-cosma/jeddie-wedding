from pathlib import Path

from config import config
from . import Base, engine
from .model import Guest, Party, Item, Gift

if config.DB_TYPE == "SQLITE":
    database_file = Path(config.SQLALCHEMY_DB_STRING.split(':', 1)[1])
    if not database_file.exists():
        database_file.touch()

Base.metadata.create_all(bind=engine)
