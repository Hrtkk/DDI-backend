from flask import (
    request, jsonify, session, Response, json
)
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from app import app, db
from app.models import User

bcrypt = Bcrypt()


@app.route("/auth/logout", methods=['GET'])
def Logout():
    print("request ", request.get_json()[
          'Email'], request.get_json()['Password'])
    return jsonify({"response": "successfull"})


@app.route("/auth/login", methods=['GET', 'POST'])
def Login():
    email = request.get_json()['email']
    password = request.get_json()['password']
    u = User.query.all()
    print(u[0].email)
    response = User.query.filter_by(email=email).first()
    print(response.email, response.password)
    if response:
        if bcrypt.check_password_hash(response.password, password):
            expires = timedelta(days=1)
            access_token = create_access_token(identity={
                'id': response.id,
                'username': response.username,
                'email': response.email
            }, expires_delta=expires)
            print(access_token)
            message = json.dumps(
                {"result": "successfully created", "access_token": access_token})
            print(message)
            resp = jsonify(message)
            return resp
        else:
            return jsonify({'success': 'false', 'error': "invalid username and password"})
    else:
        return jsonify({"response": "User does not exist", "success": "false"})


@app.route("/auth/signup", methods=['POST'])
def Signup():
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    username = request.get_json()['username']
    response = User.query.filter_by(email=email).first()
    if response:
        return jsonify({'success': 'false', 'response': 'user alreay exist'})
    else:
        id = len(User.query.all())
        u = User(id=id, email=email, password=password, username=username)
        db.session.add(u)
        db.session.commit()
        return jsonify({'success': 'true', "response": "user id created"})


# import functools
# from flask_cors import CORS, cross_origin
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from flask import jsonify
# from flask_jwt_extended import (create_access_token)
# from . import db
# from flask_bcrypt import Bcrypt
# from datetime import datetime, timedelta
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# bp = Blueprint('auth', __name__, url_prefix='/')
# bcrypt = Bcrypt()

# @bp.route('/users/register', methods=['POST'])
# def register():
#     user = db.get_db().users
#     print(user.find_one())
#     fname = request.get_json()['firstName']
#     lname = request.get_json()['lastName']
#     email = request.get_json()['email']
#     password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
#     username = request.get_json()['userName']
#     created = datetime.utcnow()

#     user_id = user.insert({
#         'userName': username,
#         'firstName': fname,
#         'lastName': lname,
#         'email': email,
#         'password': password,
#         # 'created': created,
#         'CustomerId':user.count()+1
#     })
#     print(user_id)
#     new_user = user.find_one({'_id': user_id})
#     print(new_user)
#     print(new_user['email'])
#     result = {'email': new_user['email'] + " registered"}
#     return jsonify({'result': result})

# @bp.route('/users/login', methods=['POST'])
# def login():
#     print("Hello")
#     users = db.get_db().users
#     email = request.get_json()['email']
#     password = request.get_json()['password']
#     result = ""
#     response = users.find_one({'email': email})
#     print(response)
#     print(bcrypt.check_password_hash(response['password'], password))
#     if response:
#         if bcrypt.check_password_hash(response['password'], password):
#             print("reached")
#             expires = timedelta(days=1)
#             access_token = create_access_token(identity={
#                 'CustomerId': response['CustomerId'],
#                 'firstName': response['firstName'],
#                 'lastName': response['lastName'],
#                 'email': response['email']
#             },expires_delta=expires)
#             print(access_token)
#             result = jsonify(access_token=access_token)
#         else:
#             result = jsonify({'error': "invalid username and password"})
#     else:
#         result = jsonify({'result': "No result found"})
#     return result
