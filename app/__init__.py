from .config import Config
from flask import Flask 
from .routes import routes_bp
from .models import db, migrate
from app.helpers import mail, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app)

    # Initialize the mail extension
    mail.init_app(app)

    # Initialize the bcrypt extension
    bcrypt.init_app(app)

    # Register the blueprints
    app.register_blueprint(routes_bp)

    return app