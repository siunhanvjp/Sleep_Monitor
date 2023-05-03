import json
from dict import db
from dict import bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
import datetime
from flask_jwt_extended import get_current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'User {self.username}'
    

    
class SleepLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sleepTime = db.Column(db.String)
    wakeTime = db.Column(db.String)
    temp = db.Column(db.Float)
    humid = db.Column(db.Float)
    light = db.Column(db.Float)
    quality = db.Column(db.String) #1 good, 0 bad
    username = db.Column(db.String, db.ForeignKey('user.username'),nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "sleeptime": self.sleepTime, "awaketime": self.wakeTime, "temp": self.temp, "humid": self.humid, "light": self.light, "quality": self.quality}

 
