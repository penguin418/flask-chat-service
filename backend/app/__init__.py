#!/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo


socketio = SocketIO()
app = None


def create_app(debug=False):
    global app
    app = Flask(__name__)
    app.debug = debug
    
    # mongodb 설정 // mongodb setting
    app.config["MONGO_URI"] = "mongodb://root:changelater@192.168.99.100:27017/test?authSource=admin"
    app.config['MONGO_AUTH_SOURCE'] = 'admin'
    mongo = PyMongo(app)
    app.db = mongo.db

    @app.route('/')
    def index():
        return render_template('index.html')
    
    from .mod_chat import mod_chat as chat
    app.register_blueprint(chat)
    
    from .mod_auth import mod_auth as auth
    app.register_blueprint(auth)
    
    socketio.init_app(app)
    return app
    
    