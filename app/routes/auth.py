from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.helpers import get_student_details
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()    
    if form.validate_on_submit():
        # Login logic here
        return redirect(url_for('routes.index.index'))
    return render_template('login.html', form=form)
    
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
        
    if form.validate_on_submit():
        roll_no = form.roll_no.data
        password = form.password.data

        try:
            student = get_student_details(roll_no)
            if student is None:
                flash('Invalid roll number', 'danger')
                return redirect(url_for('routes.auth.register'))
            elif student['E-Mail'] == '':
                flash('Email not found', 'danger')
                return redirect(url_for('routes.auth.register'))
        except Exception as e:
            flash('Invalid roll number', 'danger')
            return redirect(url_for('routes.auth.register'))
        # Verify if the user is already registered
        # If not, send an email to the user with a link to verify their email
        return redirect(url_for('routes.login.index'))
    return render_template('register.html', form=form)