from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app.helpers import bcrypt, get_student_details
from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='gbm')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        CheckConstraint('role IN ("gbm", "contributor", "admin")', name='role_check'),
    )

    @hybrid_property
    def is_authenticated(self):
        return True

    @hybrid_property
    def is_anonymous(self):
        return False

    @hybrid_property
    def is_active(self):
        return self.is_active
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_contributor(self):
        return self.role == 'contributor'

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '<User %r>' % self.username