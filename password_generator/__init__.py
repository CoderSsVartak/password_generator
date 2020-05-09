from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "srm@2403_vartak"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from password_generator import routes