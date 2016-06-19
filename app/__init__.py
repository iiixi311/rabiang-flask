# -*- coding: utf-8 -*-
import logging
import logging.handlers

from flask import Flask, g, request, current_app, render_template
from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

# Flask Extensions can be references as global variable.
db = SQLAlchemy()
babel = Babel()
csrf = CsrfProtect()
login_manager = LoginManager()


def create_app(config=None, app_name=None, blueprints=None):
    # Create Flask App instance
    app_name = app_name or __name__
    app = Flask(app_name)
    app.config.from_pyfile(config)

    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)
    configure_cli(app)

    return app


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_extensions(app):
    """Initialize Flask Extensions."""
    db.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    @babel.localeselector
    def get_locale():
        # If logged in, load user locale settings.
        user = getattr(g, 'user', None)

        if user is not None:
            return user.locale

        # Otherwise, choose the language from user browser.
        return request.accept_languages.best_match(current_app.config['BABEL_LANGUAGES'].keys())

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)

        if user is not None:
            return user.timezone


def configure_logging(app):
    """Configure rotating file(info) logging."""
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler = logging.handlers.RotatingFileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def configure_error_handlers(app):
    # http://flask.pocoo.org/docs/latest/errorhandling/

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('default/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('default/500.html'), 500


def configure_cli(app):
    @app.cli.command()
    def initdb():
        """Initialize database setup."""
        db.drop_all()
        db.create_all()

    @app.cli.command()
    def test():
        """Run the unit tests."""
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
