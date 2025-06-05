"""
Wedding website application package.

This package contains a Flask application for managing a wedding website with RSVP
functionality and a gift registry with Stripe integration. The application supports
both English and Romanian languages.
"""

import os

from flask import Flask, g, redirect, url_for

from config import config


def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application with the following features:
    - Creates the instance folder if it doesn't exist
    - Loads configuration from config.py
    - Registers blueprints for frontend, backend, and error handlers
    - Sets up the root route with language redirection
    - Configures database cleanup on application context teardown

    Returns:
        Flask: The configured Flask application instance
    """
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
    from jeddie.exceptions import error_handlers
    app.register_blueprint(error_handlers)

    @app.route('/')
    def index():
        """
        Root route handler that redirects to the language-specific home page.
        
        Sets the default language to English and redirects to the main index page.
        
        Returns:
            Response: A redirect response to the language-specific home page
        """
        g.language_code = 'en'
        return redirect(url_for('jeddie.index'), code=302)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        """
        Cleanup function that runs after each request.
        
        Ensures database connections are properly closed after each request.
        
        Args:
            resp_or_exc: The response or exception that was raised during request handling
            
        Returns:
            The original response or exception
        """
        if db := g.pop('db', None):
            db.close()

    return app
