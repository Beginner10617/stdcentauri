from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(6), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    __table_args__ = (
        CheckConstraint('is_active IN (0, 1)', name='is_active_check'),
        CheckConstraint('is_admin IN (0, 1)', name='is_admin_check'),
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

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username