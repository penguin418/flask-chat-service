from . import mod_chat
from .. import socketio as io, app
from ..schemas.schema_chat import validate_new_chat
from ..utils.error_handler import request_should_be_json, request_does_not_match_expected_format


from flask import render_template, request, redirect, url_for, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_socketio import emit, join_room, leave_room
from time import time
import secrets

authorized = ['1', '2', '3']


@mod_chat.route('/<room_id>')
def room(room_id):
    # 가입된 방인지 확인 // check if user can enter the room
    if room_id not in authorized:
        return redirect('/')
    return render_template('chat-room.html', room_id=room_id)


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
    data['timestamp'] = time()
    emit(
        'broadcast msg',
        data,
        room=data['room']
    )


@io.on('disconnect')
def onDisconnect():
    print('disconnected')


class ChatsListAPI(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        cursor = app.db['chats'].find(
            {'members.username': identity['username']},
        )
        chats = [cur for cur in cursor]
        res = jsonify({'chats': chats})
        if not len(chats):
            return make_response(res, 200)
        return make_response(res, 200)

    @jwt_required
    def post(self):
        # post 처리
        if not request.is_json:
            return request_should_be_json()

        data = request.get_json()
        success, data = validate_new_chat(data)
        if not success:
            return request_does_not_match_expected_format(data)

        data['room_id'] = secrets.token_hex(nbytes=64)
        app.db['chats'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!', 'data': data})
        return make_response(res, 200)


class ChatsAPI(Resource):
    @jwt_required
    def get(self, room_id):
        res = {'room_id': room_id, 'exist': False}

        candidate = app.db['chatrooms'].find_one(
            {'room_id': room_id},
            {'_id': 0}
        )
        if candidate:
            res['id'] = str(candidate['_id'])
            res['exist'] = True
            return make_response(jsonify(res), 200)
        else:
            return jsonify(res), 404

    @jwt_required
    def put(self, room_id):
        title = request.args.get('title')
        app.db['chats'].update({'room_id': room_id}, {"$set": {"title": title}})
        res = jsonify({'title': title, 'success': '변경되었습니다 // updated successfully'})
        return make_response(res, 200)

    @jwt_required
    def delete(self, room_id):
        identity = get_jwt_identity()
        app.db['chats'].update(
            {'room_id': room_id},
            {"$pull": {"members.username": identity['username']}}
        )
        res = jsonify({'room_id': room_id, 'success': '나왔습니다 // came out successfully'})
        return make_response(res, 200)
