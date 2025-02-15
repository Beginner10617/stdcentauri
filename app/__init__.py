from .config import Config
from flask import Flask 
from .routes import routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register the blueprints
    app.register_blueprint(routes_bp)

    return app