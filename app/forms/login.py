from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    roll_no = StringField('Roll no', validators=[DataRequired(), Length(min=6, max=6)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')