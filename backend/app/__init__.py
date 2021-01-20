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


def create_app(configs = [], debug=False):
    global app
    app = Flask(__name__)
    for config in configs:
        app.config.update(config)
    app.debug = app.config['debug']

    app.config['MONGO_URI'] = 'mongodb://%s:%s@%s:%s/%s?authSource=%s' % (
        app.config['MONGO_USERNAME'],
        app.config['MONGO_PASSWORD'],
        app.config['MONGO_HOST'],
        app.config['MONGO_PORT'],
        app.config['MONGO_DBNAME'],
        app.config['MONGO_AUTH_SOURCE']
    )
    mongo = PyMongo(app)
    app.db = mongo.db

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
    
    