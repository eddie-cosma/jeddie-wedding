from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


engine = create_engine(current_app.config['SQLALCHEMY_DB_STRING'], echo=True, future=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
