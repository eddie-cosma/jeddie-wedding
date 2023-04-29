import os

from flask import Flask, g, redirect, url_for

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
    from jeddie.routes import backend_bp
    app.register_blueprint(backend_bp)

    @app.route('/')
    def index():
        g.language_code = 'en'
        return redirect(url_for('jeddie.index'), code=302)

    @app.route('/rsvp')
    def rsvp():
        g.language_code = 'en'
        return redirect(url_for('jeddie.rsvp'), code=302)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        if db := g.pop('db', None):
            db.close()

    return app
