from flask import redirect, render_template, url_for, flash, request
from password_generator import app, db, db_session
from password_generator.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from password_generator.models import User
from password_generator.Security.security_qns import Security_question
from password_generator.forms import ValidationError


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
        #print("User: ",user.username, user.password)
        #print("Password", form.password.data, form.username.data)
        
        #If user is not found
        if user == None:
            form.username.errors = "Invalid User"
            return render_template('login.html', form=form)

        if form.password.data == user.password:
            login_user(user)
            print(db_session.create_session(user.username))
            print("DOne")
            return redirect(url_for('dashboard'))

        #If password does not match
        else:
            form.password.errors = "Password Mismatch"
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():

    #If user is already logged in then do not let the user go back to login page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    #Security qns taken out from the list of security questions
    s = Security_question()
    qns = s.read_qns()

    form = RegistrationForm()
    print(form.validate_on_submit())
    if request.method == 'POST':

        #Get the data entered by the user
        form.username.data = request.form['user_ip']
        form.email.data = request.form['email_ip']
        form.fullname.data = request.form['fname_ip']
        form.password.data = request.form['password_ip']
        #form.confirm_password.data = request.form['repassword_ip']
        form.contact.data = request.form['phn_ip']
        form.sec_qns.data = request.form['security_qns']
        form.sec_ans.data = request.form['security_qns_ans']

        #Encrypt password before adding to the database

        #Create object for user
        user = User(name=form.fullname.data, username=form.username.data, email=form.email.data,
                     contact=form.contact.data, password=form.password.data, sec_qns=form.sec_qns.data, sec_ans=form.sec_ans.data)
        
       
        #If the username is already taken     
        try:
            form.validate_username(form.username)
        except ValidationError:
            form.username.errors = ["Username already taken"]
            return render_template('register.html', form=form, sec_qns=qns)

        #if the email is already registered
        try:
            form.validate_email(form.email)
        except ValidationError:
            form.username.errors = ["Email Already Exists. Please choose a valid Email Address"]
            return render_template('register.html', form=form, sec_qns=qns)

        #If all checks are successfull
        #Add user to database and send him to login page
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    
    return render_template('register.html', form=form, sec_qns=qns)


@app.route("/dashboard")
@login_required
def dashboard():
    print(current_user.username)
    return render_template('dashboard.html', username=current_user.username)


@app.route("/logout")
def logout():
    print("Logged Out", current_user)
    db_session.end_session(current_user.username)
    logout_user()
    return redirect(url_for('index'))