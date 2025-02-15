from flask import Blueprint
from .index import index_bp
from .auth import auth_bp

routes_bp = Blueprint('routes', __name__)

# Register the blueprints
routes_bp.register_blueprint(index_bp)
routes_bp.register_blueprint(auth_bp)