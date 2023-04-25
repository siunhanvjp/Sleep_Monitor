import json
from dict import db
from dict import bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
import datetime
from flask_jwt_extended import get_current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    
    def __repr__(self):
        return f'User {self.username}'
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    
class SleepLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sleeptime = db.Column(db.String)
    awaketime = db.Column(db.String)
    temp = db.Column(db.Float)
    humid = db.Column(db.Float)
    light = db.Column(db.Float)
    quality = db.Column(db.Integer) #1 good, 0 bad
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "sleeptime": self.sleeptime, "awaketime": self.awaketime, "temp": self.temp, "humid": self.humid, "light": self.light, "quality": self.quality}

 
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id'),
        default=lambda: get_current_user().id,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
    )
