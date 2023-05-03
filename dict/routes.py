import datetime
from datetime import datetime, timezone, timedelta
import json
from dict import app, db, os, jwt
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from dict.models import User, SleepLog
from dict.forms import LoginForm, SearchForm
from flask_paginate import get_page_parameter
from flask_sqlalchemy import Pagination
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, current_user, JWTManager


    
@app.route('/user', methods=["GET"])
def get_user():                                         
    username = request.args.get("username")
    attempted_user = User.query.filter_by(username=username).one_or_none()
    if attempted_user is None:
        res = []
    else:
        id = attempted_user.id
        password = attempted_user.password
        res = [
            {
                'id': id,
                'username': username,
                'password': password
            }
        ]
    return jsonify(res)
 
@app.route('/user', methods=["POST"])   
def add_user():    
    try:                                     
        username = request.json.get("username")
        password = request.json.get("password")
        user_to_create = User(username=username,
                            password=password)
        db.session.add(user_to_create)
        db.session.commit()
        return jsonify({"status": "OKE"})
    except Exception as e:
        print(e)
        return jsonify({"status": "Fail"})
    
@app.route('/history', methods=["GET"])   
def get_history():    
    username = request.args.get("username")
    requested_history = SleepLog.query.filter_by(username = username).order_by(SleepLog.id.asc()).all()
    res = []
    for log in requested_history:
        item = {
            "sleepTime": log.sleepTime,
            "wakeTime": log.wakeTime,
            "temp": log.temp,
            "humid": log.humid,
            "light": log.light,
            "quality": log.quality,
            "username": log.username,
            "id": log.id,
        }
        res.append(item)
    return jsonify(res)

@app.route('/history', methods=["POST"])   
def add_history():    
    try: 
        sleepTime = request.json.get("sleepTime")
        wakeTime = request.json.get("wakeTime")
        temp = request.json.get("temp")
        humid = request.json.get("humid")
        light = request.json.get("light")
        quality = request.json.get("quality")
        username = request.json.get("username")

        log_to_create = SleepLog(sleepTime=sleepTime,
                                wakeTime=wakeTime,
                                temp=temp,
                                humid=humid,
                                light=light,
                                quality=quality,
                                username=username)
        db.session.add(log_to_create)
        db.session.commit()
        return jsonify({"status": "OKE"})
    except Exception as e:
        print(e)
        return jsonify({"status": "Fail"})
    
@app.route('/history/<int:hisID>', methods=["PATCH"])   
def modify_history(hisID): 
    try:   
        id = hisID
        quality = request.json.get("quality")
        requested_log = SleepLog.query.filter_by(id = id).one_or_none()
        if requested_log:
            requested_log.quality = quality
            db.session.commit()
        return jsonify({"status": "OKE"})
    except Exception as e:
        print(e)
        return jsonify({"status": "Fail"})

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)   


    

