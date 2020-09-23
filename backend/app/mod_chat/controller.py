from flask import render_template, request, redirect, url_for, request
from . import mod_chat
from flask_socketio import emit, join_room, leave_room
from .. import socketio as io
from time import time

authorized = ['1', '2', '3']

@mod_chat.route('/<room_id>')
def chatroom(room_id):
    # 가입된 방인지 확인 // check if user can enter the room
    if room_id not in authorized:
        return redirect('/')
    return render_template('chatroom.html', room_id=room_id)

@io.on('subscribe')
def join(data):
    print('subscribe ', data['room'], request.sid)
    join_room(data['room'])

@io.on('unsubscribe')
def leave(data):
    print('unsubscribe ', data['room'], request.sid)
    leave_room(data['room'])

@io.on('send msg')
def send_msg(data):
    print(data)
    data['timestamp'] = time()
    emit(
        'broadcast msg', 
        data,
        room=data['room']
        )

io.on('disconnect')
def onDisconnect():
    print('disconnected')