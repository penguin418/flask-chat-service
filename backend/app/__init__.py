#!/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO

socketio = SocketIO()
app = None

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    @app.route('/')
    def index():
        return render_template('index.html')

    socketio.init_app(app)
    return app