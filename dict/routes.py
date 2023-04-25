import datetime
from datetime import datetime, timezone, timedelta
import json
from dict import app, db, os, jwt
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from dict.models import User, TokenBlocklist, SleepLog
from dict.forms import RegisterForm, LoginForm, SearchForm
from flask_paginate import get_page_parameter
from flask_sqlalchemy import Pagination
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, current_user, JWTManager


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

@app.after_request 
def refresh_expiring_jwts(response): #used to refresh token :D just ignore this part :D
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes = 15))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

#send POST to this url, JSON format 
# {
#     "username": ???,
#     "password": ???
# }
@app.route('/api/login', methods=["POST"])
def create_token():                                         
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    attempted_user = User.query.filter_by(username=username).one_or_none()
    if attempted_user and attempted_user.check_password_correction(attempted_password=password):
        access_token = create_access_token(identity=attempted_user) #create token
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid username or password"}), 401   

#send DELETE, remember to include in request's Header: Authorization: Bearer <token>
@app.route("/api/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def modify_token():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


#send POST to this url, json format 
# {
#     "username": ???,
#     "email_address": ???,
#     "password1": ???,
#     "password2": ???
# }
@app.route("/api/register", methods=['POST'])
def api_register():
    form = RegisterForm()
    form.username.data = request.json.get("username", None)
    form.email_address.data = request.json.get("email_address", None)
    form.password1.data = request.json.get("password1", None)
    form.password2.data = request.json.get("password2", None)   #inject data to form
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return jsonify({"msg": "create success !!!!!"})  
    if form.errors != {}:
        output = []
        for err_msg in form.errors.values():
            user_err = {}
            user_err['msg'] = f'There was an error: {err_msg}'
            output.append(user_err)
        return jsonify({'err': output})
    return jsonify({"msg": "create success ?"})        

#send GET to this url, json format 
# {
#       "id": ??? 
# }

@app.route("/api/get_data", methods=["GET"])
def get_sleeplog():
    log_id = request.json.get('id')
    try:
        requested_log = SleepLog.query.filter_by(id = log_id).first().to_dict()
        return jsonify({"status": "success", "log": requested_log})
    except Exception as e:
        return jsonify({"status": "fail"})

#send POST to this url, json format 
# {
#     "sleeptime": ???,
#     "awaketime": ???,
#     "temp": ???,
#     "humid": ???,
#     "light": ???,
#     "quality": ???,
#     "user_id": ??? 
# }

@app.route("/api/add_data", methods=['POST'])
def add_sleeplog():
    try:
        sleeplog_to_create = SleepLog(sleeptime = request.json.get("sleeptime", None),
                                    awaketime = request.json.get("awaketime", None),
                                    temp = request.json.get("temp", None),
                                    humid = request.json.get("humid", None),
                                    light = request.json.get("light", None),
                                    quality = request.json.get("quality", None),
                                    user_id = request.json.get("user_id", None),
                                    # user_id = current_user.id,
                                    )
        db.session.add(sleeplog_to_create)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print(f'error: {e}')
        return jsonify({"status": "fail"})
        
    
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)   


    

