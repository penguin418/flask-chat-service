#!/bin/env python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from time import time


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

    @socketio.on('subscribe')
    def subscribe(data):
        print('subscribe ', data['room'], request.sid)
        join_room(data['room'])

    @socketio.on('unsubscribe')
    def unsubscribe(data):
        print('unsubscribe ', data['room'], request.sid)
        leave_room(data['room'])

    @socketio.on('send msg')
    def send_msg(data):
        print(data)
        data['timestamp'] = time()
        emit(
            'broadcast msg', 
            data,
            room=data['room']
            )
            
    return app