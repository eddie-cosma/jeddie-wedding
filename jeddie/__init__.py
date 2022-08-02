import os

from flask import Flask, g

from config import config


def create_app():
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_object(config)

    from jeddie.routes import frontend_bp
    app.register_blueprint(frontend_bp)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        if db := g.pop('db', None):
            db.close()

    return app
