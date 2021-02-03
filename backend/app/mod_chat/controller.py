from sqlalchemy import Date

from . import mod_chat
from .. import socketio as io, app
from ..schemas.schema_chat import validate_new_room, validate_new_msg
from ..utils.error_handler import request_should_be_json, request_does_not_match_expected_format

from flask import render_template, request, redirect, url_for, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_socketio import emit, join_room, leave_room, send
from datetime import datetime, timezone
import secrets

@jwt_required
@io.on('join room')
def on_join_room(data):
    print('join room', data)
    join_room(data['room_id'])


@jwt_required
@io.on('leave room')
def on_leave_room(data):
    leave_room(data['room_id'])


@jwt_required
@io.on('send msg')
def on_send_msg(data):
    print(data)
    success, data = validate_new_msg(data)
    if not success:
        send('request_does_not_match_expected_format')

    data['timestamp'] = str(datetime.utcnow().timestamp())
    for member in data['members']:
        member['read'] = False
        if member['username'] == data['sender']:
            member['read'] = True

    app.db['msgs'].insert_one(data)
    data['_id'] = str(data['_id'])
    emit('broadcast msg', {'data': data}, room=data['room_id'])

@jwt_required
@io.on('flag read')
def on_flag_read(data):
    data['']

@jwt_required
@io.on('load msg')
def on_load_msg(data):
    cursors = app.db['msgs'].find({
        'room_id': data['room_id'],
        'members': data['username'],
        'timestamp': {'$lt': data['timestamp']}
    }).limit(50)
    msgs = [cursor for cursor in cursors]
    for msg in msgs:
        msg['_id'] = str(msg['_id'])
    send(jsonify({'data': msgs}))

class RoomsListAPI(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        cursor = app.db['rooms'].find(
            {'members.username': identity['username']},
        )
        chats = [cur for cur in cursor]
        for chat in chats:
            chat['_id'] = str(chat['_id'])
        return make_response(jsonify({'success': '%d개의 대화가 저장되어있습니다' % len(chats), 'data': chats}), 200)

    @jwt_required
    def post(self):
        # post 처리
        if not request.is_json:
            return request_should_be_json()

        data = request.get_json()
        success, data = validate_new_room(data)
        if not success:
            return request_does_not_match_expected_format(data)

        app.db['rooms'].insert_one(data)
        data['_id'] = str(data['_id'])
        res = jsonify({'success': '등록되었습니다 // registered successfully!', 'data': data})
        return make_response(res, 200)


class RoomsAPI(Resource):
    @jwt_required
    def get(self, room_id):
        res = {'room_id': room_id, 'exist': False}

        candidate = app.db['rooms'].find_one(
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
        app.db['rooms'].update_one({'room_id': room_id}, {"$set": {"title": title}})
        res = jsonify({'title': title, 'success': '변경되었습니다 // updated successfully'})
        return make_response(res, 200)

    @jwt_required
    def delete(self, room_id):
        identity = get_jwt_identity()
        app.db['rooms'].update_one(
            {'room_id': room_id},
            {"$pull": {"members.username": identity['username']}}
        )
        res = jsonify({'room_id': room_id, 'success': '나왔습니다 // came out successfully'})
        return make_response(res, 200)
