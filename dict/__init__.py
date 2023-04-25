import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

# from flask_ngrok import run_with_ngrok
app = Flask(__name__)
CORS(app)

dir = os.path.dirname(__file__)

dir_db = os.path.join(dir,'dict.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ dir_db
app.config['SECRET_KEY'] ='1b253b240b0a78e764b9ec90'
app.config["JWT_SECRET_KEY"] = "DW8jOOS4JC0zaseOb9jgaIYVsnkmVseHXhSgfICKBqNHuUJTmBB7dmpz6Bzcgqt"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) #set time for token expiration
app.config['WTF_CSRF_ENABLED'] = False #disable csrf

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)                                   # recently added
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@jwt.user_identity_loader                               # recently added
def user_identity_lookup(user):
    return user.id    
    
@jwt.user_lookup_loader                                 # recently added 
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


from dict import routes
from .models import User, SleepLog

with app.app_context():
    db.create_all()
    print('Created Database!')


