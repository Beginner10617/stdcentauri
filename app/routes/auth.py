from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.helpers import get_student_details, send_verification_email
from app.models import User, db
import jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()    
    if form.validate_on_submit():
        # Login logic here
        return redirect(url_for('routes.index.index'))
    return render_template('login.html', form=form)
    
pending_users = {}

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
        
    if form.validate_on_submit():
        roll_no = form.roll_no.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('routes.auth.register'))
        try:
            student = get_student_details(roll_no)
            if student is None:
                flash('Invalid roll number', 'danger')
                return redirect(url_for('routes.auth.register'))
            elif student['E-Mail'] == '':
                flash('Email not found', 'danger')
                return redirect(url_for('routes.auth.register'))
            else:
                email = student['E-Mail']
                name = student['Name']
        except Exception as e:
            flash('Invalid roll number', 'danger')
            return redirect(url_for('routes.auth.register'))
        # Verify if the user is already registered
        user = User.query.filter_by(roll_no=roll_no).first()
        if user:
            flash('User already registered', 'danger')
            return redirect(url_for('routes.auth.register'))

        user = User(roll_no=roll_no, name=name, email=email)
        user.set_password(password)
        pending_users[email]=user
        flash('Account created successfully. Please check your email to verify your account.', 'success')
        send_verification_email(user)
        
        return redirect(url_for('routes.auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    try:
        # Decode the token to get the email
        data = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        email = data['email']
        
        # Mark the user's email as verified
        if email in pending_users:
            user = pending_users.pop(email)
            flash('Your email has been verified!', 'success')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('routes.auth.login'))
    except jwt.ExpiredSignatureError:
        flash('The verification link has expired', 'error')
    except jwt.InvalidTokenError:
        flash('Invalid verification link', 'error')
    return redirect(url_for('routes.auth.login'))