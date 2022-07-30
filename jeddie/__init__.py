from flask import Flask

from .database import Base, Session
from jeddie.routes import frontend_guest


def create_app():
    app = Flask(__name__)
    app.register_blueprint(frontend_guest)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    return app
