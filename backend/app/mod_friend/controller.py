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


class FriendsAPI(Resource):

    # @jwt_required
    def get(self):
        """
        username 존재하는 경우 해당 user가 존재하는지 알려줌
        그렇지 않으면 친구 목록을 돌려줌
        """
        username = request.args.get('username')
        if username:
            result = { 'username': username, 'exist': False }

            candidate = app.db['users'].find_one({'username': username})
            if candidate:
                result['id'] = str(candidate['_id'])
                result['exist'] = True
                return make_response(jsonify(result), 200)
            else:
                return jsonify(result), 404
        else:
            identity = get_jwt_identity()
            cursor = app.db['friends'].find({'requester.friend_id': identity['id'] }, {"_id":0,"subject":1})
            friends = [cur for cur in cursor]
            print(friends)
            if not len(friends):
                return make_response(jsonify({'friends':friends}), 200)
            return make_response(jsonify({'friends':friends}), 200)

    # @jwt_required
    def post(self):
        """
        친구 추가
        :return:
        """
        print(request.is_json)
        print(request.get_data())
        if not request.is_json:
            return make_response(jsonify({"error": "요청은 json이어야 합니다 request should be JSON"}), 400)
        print(3)
        success, data = validate_new_friend(request.get_json())
        print(4)
        if not success:
            return make_response(jsonify({"login": False, 'error': str(data)}), 400)

        data['status'] = 0
        app.db['friends'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!'})
        return make_response(res, 200)


# @mod_friend.route('/', methods=['GET'])
# def friends_list():
#     username = request.args.get('username')
#     if username:
#         result = { 'username': username, 'exist': False }
#
#         candidate = app.db['users'].find_one({'username': username})
#         if candidate:
#             result['exist'] = True
#             return jsonify(result), 200
#         else:
#             return jsonify(result), 404
#     else:
#         identity = get_jwt_identity()
#         friends = app.db['friends'].find({'requester.id': identity['id']})
#         print(friends.explain())
#         if not len(friends):
#             return jsonify('frineds', []), 200
#         return jsonify('friends', friends), 200
#
# @mod_friend.route('/new', methods=['POST'])
# @jwt_required
# def frined_add():
#     identity = get_jwt_identity()
#     # post 처리
#     if not request.is_json:
#         return jsonify({"error": "요청은 json이어야 합니다 // request should be JSON"}), 400  # Bad Request
#
#     success, data = validate_new_friend(request.get_json())
#     if not success:
#         return jsonify({'error': str(data)}), 400
#
#     app.db['friends'].insert_one()
#     return res, 200
#
#
# @mod_friend.route('/friends/delete', methods=['delete'])
# @jwt_required
# def friend_delete():
#     identity = get_jwt_identity()
#     print('identity', identity)
#     res = jsonify({'delete', 200})
#     return res, 200
