from pathlib import Path

from config import config
from . import Base, engine
from .model import Guest, Party, Address

database_file = Path(config.SQLALCHEMY_DB_STRING.split(':', 1)[1])
if not database_file.exists():
    database_file.touch()

Base.metadata.create_all(bind=engine)