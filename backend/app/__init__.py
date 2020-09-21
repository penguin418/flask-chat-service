#!/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


socketio = SocketIO()
app = None

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    @app.route('/')
    def index():
        return render_template('index.html')

    # socketio 코드 시작 // start socketio code
    socketio.init_app(app)

    @socketio.on('send msg')
    def send_msg(data):
        print(data)
        emit('broadcast msg', data, broadcast=True)
        
    return app