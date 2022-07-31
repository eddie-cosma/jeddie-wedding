import json
import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_file("config.json", load=json.load)

    with app.app_context():
        from .database import Base, Session
        from jeddie.routes import frontend_bp

    app.register_blueprint(frontend_bp)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    return app
