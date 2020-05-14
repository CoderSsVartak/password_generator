from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from password_generator.Database.active_sessions import Active_Sessions
from password_generator.Database.my_space import My_Space
from password_generator.Security.encrypt import encryption

app = Flask(__name__)
app.secret_key = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db_session = Active_Sessions()
space = My_Space()
e = encryption(app.secret_key)

from password_generator import routes