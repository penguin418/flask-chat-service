from .. import app
from ..schemas.schema_friend import validate_new_friend
from .. import socketio as io

from flask import render_template, request, jsonify, make_response
import flask_bcrypt
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
    jwt_required,
    get_jwt_identity, jwt_refresh_token_required,
    get_csrf_token, unset_jwt_cookies,
)
import jsonschema
from bson.dbref import DBRef
from flask_restful import Resource
from bson.json_util import dumps
from bson.json_util import loads
from bson import json_util

from ..utils.error_handler import request_should_be_json, request_does_not_match_expected_format


class FriendsListApi(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        cursor = app.db['friends'].find(
            {'requester.username': identity['username']},
            {"_id": 0, "subject": 1}
        )
        friends = [cur for cur in cursor]
        res = jsonify({'friends': friends})
        if not len(friends):
            return make_response(res, 200)
        return make_response(res, 200)

    @jwt_required
    def post(self):
        """
        친구 추가
        :return:
        """
        if not request.is_json:
            return request_should_be_json()

        success, data = validate_new_friend(request.get_json())
        if not success:
            return request_does_not_match_expected_format(data)

        if data['subject']['username'] == get_jwt_identity()['username']:
            return make_response({'error': '자기 자신을 친구로 등록할 수 없습닏다 // cannot register yourself as a friend'})

        data['status'] = 0
        app.db['friends'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!'})
        return make_response(res, 200)


class FriendsAPI(Resource):

    @jwt_required
    def get(self, username):
        """
        username 존재하는 경우 해당 user가 존재하는지 알려줌
        """
        res = {'username': username, 'exist': False}

        candidate = app.db['users'].find_one({'username': username})
        if candidate:
            res['id'] = str(candidate['_id'])
            res['exist'] = True
            return make_response(jsonify(res), 200)
        else:
            return jsonify(res), 404

    @jwt_required
    def delete(self, username):
        """
        친구 삭제
        :return:
        """

        identity = get_jwt_identity()
        app.db['friends'].delete_one(
            {"register.username": identity['username'],
             "subject.username": username}
        )
        return make_response('OK', 200)