from flask import Flask
from .routes import pages, api

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    return app
