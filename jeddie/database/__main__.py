from . import Base, engine
from .model import Guest, Party, Address

Base.metadata.create_all(bind=engine)