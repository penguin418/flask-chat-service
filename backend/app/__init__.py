#!/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import json
import datetime

socketio = SocketIO()
app = None


def create_app(debug=False):
    global app
    app = Flask(__name__)
    app.debug = debug
    
    # mongodb 설정 // mongodb setting
    app.config["MONGO_URI"] = "mongodb://root:changelater@localhost:27017/test?authSource=admin"
    app.config['MONGO_AUTH_SOURCE'] = 'admin'
    mongo = PyMongo(app)
    app.db = mongo.db

    # jwt인증 // jwt
    app.config['JWT_SECRET_KEY'] = 'changelater'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['JWT_COOKIE_SECURE'] = False # false allow http
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    JWT_COOKIE_CSRF_PROTECT = True 
    flask_bcrypt = Bcrypt(app)
    app.json_encoder = json.JSONEncoder
    jwt = JWTManager(app)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    from .mod_chat import mod_chat as chat
    app.register_blueprint(chat)
    
    from .mod_auth import mod_auth as auth
    app.register_blueprint(auth)
    
    socketio.init_app(app)
    return app
    
    