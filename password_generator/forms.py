import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from password_generator.models import User



class LoginForm(FlaskForm):

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Username Already Taken.Choose a different username")
        
        elif user == None:
            raise ValidationError("Username Not Found")


class RegistrationForm(FlaskForm):

    fullname = StringField('fname_ip', validators=[DataRequired(), Length(min=2, max=120)])
    contact = StringField('phn_ip', validators=[DataRequired(), Length(min=10, max=10)])
    username = StringField('user_ip', validators=[DataRequired(), Length(min=4, max=120)])
    email = StringField('email_ip', validators=[DataRequired(), Email()])
    password = PasswordField('password_ip', validators=[DataRequired(), Length(min=5, max=120)])
    confirm_password = PasswordField('repassword_ip', validators=[DataRequired(), EqualTo('password')])
    sec_qns = StringField('security_qns', validators=[DataRequired()])
    sec_ans = StringField('security_qns_ans', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Already Taken.Choose a different username")
        if len(username.data)>45:
            raise TypeError

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            print("FOUND")
            raise ValidationError("Email Already Exists. Please choose a valid Email Address")
    def validate_contact(self, contact):

        flag = bool(re.search(r'[a-zA-Z]', contact.data) or re.search(r'\W', contact.data))
        if not len(contact.data) == 10 or flag:
            raise ValidationError("Contact Number invalid")
    
    def match_passwords(self, password, repassword):

        return password.data == repassword.data