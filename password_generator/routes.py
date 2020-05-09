from flask import redirect, render_template, url_for, flash, request
from password_generator import app, db
from password_generator.forms import LoginForm
from flask_login import login_user, current_user, login_required, logout_user
from password_generator.models import User

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():

    #If user is already logged in then do not let the user go back to login page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    #When form is submitted
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        print("User: ",user.username, user.password)
        print("Password", form.password.data, form.username.data)
        if form.password.data == user.password:
            
            login_user(user)
            print("DOne")
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/logout")
def logout():
    print("Logged Out")
    logout_user()
    return redirect(url_for('index'))