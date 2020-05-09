from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from password_generator.models import User



class LoginForm(FlaskForm):

    username = StringField('username', validators=[DataRequired(), Length(min=5, max=30)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Username Already Taken.Choose a different username")
    

class RegistrationForm(FlaskForm):

    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirmpassword', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Already Taken.Choose a different username")

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email Already Taken.Choose a different email")


