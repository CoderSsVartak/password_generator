from flask import redirect, render_template, url_for, flash, request, jsonify
from password_generator import app, db, db_session, space, e
from password_generator.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from password_generator.models import User
from password_generator.Security.security_qns import Security_question
from password_generator.forms import ValidationError
from password_generator.Security.random_pass import Random_Password
from password_generator.Emails.send_mail import Send_Mail
import random
import json



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
        
        #If user is not found
        if user == None:
            form.username.errors = "Invalid User"
            return render_template('login.html', form=form)

        if form.password.data == e.decode(user.password).decode():
            login_user(user)
            mail = Send_Mail(user.email, "otp")
            db_session.create_session(user.username)
            if mail.sent:
                db_session.add_otp(current_user.username, mail.extra)
                return(redirect(url_for('otp')))
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

        #If any errors are present then set the value of flag to false
        flag = True

        #Get the data entered by the user
        form.username.data = request.form['user_ip']
        form.email.data = request.form['email_ip']
        form.fullname.data = request.form['fname_ip']
        form.password.data = request.form['password_ip']
        form.confirm_password.data = request.form['repassword_ip']
        form.contact.data = request.form['phn_ip']
        form.sec_qns.data = request.form['qns']
        form.sec_ans.data = request.form['security_qns_ans']
        
       
        #If the username is already taken     
        try:
            form.validate_username(form.username)
            
        except ValidationError:
            form.username.errors = ["Username already taken"]
            flag = False
        except TypeError:
            form.username.errors = ["Username too long"]
            flag = False

        #if the email is already registered
        try:
            form.validate_email(form.email)
        except ValidationError:
            flag = False
            form.email.errors = ["Email Already Exists. Please choose a valid Email Address"]
            
        #If contact info is invalid
        try:
            form.validate_contact(form.contact)
        except ValidationError:
            flag = False
            form.contact.errors = ["Invalid Contact Information"]

        if not form.match_passwords(form.password, form.confirm_password):
            flag = False
            form.confirm_password.errors = ["Password Mismatch"]

        #If any errors are present
        if not flag:
            return render_template('register.html', form=form, sec_qns=qns)

        #If all checks are successfull
        #Create object for user
        user = User(name=form.fullname.data, username=form.username.data, email=form.email.data,
                     contact=form.contact.data, password=e.encode(form.password.data), sec_qns=form.sec_qns.data, sec_ans=form.sec_ans.data)

        mail = Send_Mail(user.email, "register", username=user.username)

        #Add user to database and send him to login page
        db.session.add(user)
        db.session.commit()
        #Create user's space to store their passwords
        space.create_space(user.username)
        return redirect(url_for('login'))

    
    return render_template('register.html', form=form, sec_qns=qns)

#Change the security question
@app.route('/change_qns')
def change_qns():
    s = Security_question()
    qns = s.read_qns()
    return json.dumps(qns)


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
    psswd = []
    for password in passwords:
        #Convert the encrypted password
        temp = e.decode(password[1].encode()).decode()

        psswd.append([password[0], temp, password[2]])
    
    count = 3
    if len(psswd) < 3:
        count = len(psswd)

    return(render_template('savedpasswords.html', passwords=psswd[:count]))

#Move to next page on the show password app
@app.route('/next', methods=['POST'])
@login_required
def next():

    passwords=space.show_passwords(current_user.username)
    psswd = []
    for password in passwords:
        #Convert the encrypted password
        temp = e.decode(password[1].encode()).decode()

        psswd.append([password[0], temp, password[2]])

    page = int(request.form['page'])
    start, end = 3*page, 3*(page+1)

    if end > len(psswd):
        end = len(psswd)
    elif start > len(psswd):
        return json.dumps('null')
    if start<len(psswd) and end <= len(psswd):
        return jsonify(psswd[start:end])

#Move to previous page on the show password app
@app.route('/prev', methods=['POST'])
@login_required
def prev():

    passwords=space.show_passwords(current_user.username)
    psswd = []
    for password in passwords:
        #Convert the encrypted password
        temp = e.decode(password[1].encode()).decode()

        psswd.append([password[0], temp, password[2]])

    page = int(request.form['page'])-1
    start, end = 3*(page-1), 3*(page)

    if end > len(psswd):
        end = len(psswd)
    elif start > len(psswd):
        return json.dumps('null')
    if start<len(psswd) and end <= len(psswd):
        return jsonify(psswd[start:end])



#Save a password directly from the generate password page
@app.route('/save', methods=['POST', 'GET'])
@login_required
def save():
    
    if request.method == 'POST':
        account = request.form['account_name']
        password = request.form['password']
        result = space.add_password(current_user.username, account, e.encode(password))
        if not result:
            return jsonify({'error': "Username already present"})
        return jsonify({'success': "Account added successfully"})

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():

    if request.method == 'POST':
        account = request.form['AccountName']
        result = space.delete_passwords(current_user.username, account)
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
            result = space.add_password(current_user.username, account, e.encode(password))
            
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
    db_session.end_session(current_user.username)
    logout_user()
    return redirect(url_for('index'))

@app.route("/otp", methods=['GET', 'POST'])
def otp():

    otp_error = False

    if request.method == 'POST':
        otp = request.form['otp']
        try:
            result = db_session.verify_otp(current_user.username, otp)
            if result:
                return redirect(url_for('dashboard'))
        except AttributeError:
            otp_error = "OTP has expired"
            db_session.end_session(current_user.username)   
            logout_user()         
            return render_template('login.html', otp_error = otp_error)
        
        except ArithmeticError:
            otp_error = "Entered OTP was incorrect"
    
    return render_template('otp.html', otp_error=otp_error)