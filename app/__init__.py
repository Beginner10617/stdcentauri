from .config import Config
from flask import Flask 
from .routes import routes_bp
from .models import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app)

    # Register the blueprints
    app.register_blueprint(routes_bp)

    return app