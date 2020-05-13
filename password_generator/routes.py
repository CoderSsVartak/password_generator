from flask import redirect, render_template, url_for, flash, request, jsonify
from password_generator import app, db, db_session, space
from password_generator.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from password_generator.models import User
from password_generator.Security.security_qns import Security_question
from password_generator.forms import ValidationError
from password_generator.Security.random_pass import Random_Password
import random
import json
from urllib import parse

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
            db_session.create_session(user.username)
            #print("DOne")
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
        #Create user's space to store their passwords
        space.create_space(user.username)
        return redirect(url_for('login'))

    
    return render_template('register.html', form=form, sec_qns=qns)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@app.route('/generatepassword')
@login_required
def generatepassword():

    return(render_template('generatepassword.html'))

#send data to generatepassword page for new password without refresh 
@app.route('/anotherpassword')
@login_required
def anotherpassword():

    r = Random_Password(random.randint(8, 16))
    return json.dumps(r.password)



#Show the saved passwords
@app.route('/savedpasswords')
@login_required
def savedpasswords():

    passwords=space.show_passwords(current_user.username)
    #print(passwords)
    return(render_template('savedpasswords.html', passwords=passwords))


#Save a password directly from the generate password page
@app.route('/save', methods=['POST', 'GET'])
@login_required
def save():
    
    if request.method == 'POST':
        account = request.form['account_name']
        password = request.form['password']
        result = space.add_password(current_user.username, account, password)
        print(result)
        if not result:
            return jsonify({'error': "Username already present"})
        return jsonify({'success': "Account added successfully"})

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():

    if request.method == 'POST':
        account = request.form['AccountName']
        result = space.delete_passwords(current_user.username, account)
        print(result)
        if not result:
            return render_template('delete.html', account_error=True)
        else:
            return redirect(url_for('dashboard'))
    return render_template('delete.html')


@app.route('/storepasswords', methods=['GET', 'POST'])
@login_required
def storepasswords():

    if request.method == 'POST':

        account = request.form['AccountName']
        password = request.form['password']
        confirm_password = request.form['repassword']

        if password == confirm_password:
            result = space.add_password(current_user.username, account, password)
            
            #If account already exists
            if not result:
                return render_template('storepasswords.html', account_error=True)    
        #If passwords do not match
        else:
            return render_template('storepasswords.html', password_error=True)
        return(redirect(url_for('dashboard')))

    return(render_template('storepasswords.html'))



@app.route("/logout")
def logout():
    print("Logged Out", current_user)
    db_session.end_session(current_user.username)
    logout_user()
    return redirect(url_for('index'))