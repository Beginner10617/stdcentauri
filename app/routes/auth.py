from flask import Blueprint, request, render_template, redirect, url_for
from app.forms import LoginForm
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)