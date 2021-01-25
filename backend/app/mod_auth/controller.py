from . import mod_auth
from .. import app
from ..schemas import validate_register, validate_login
from ..utils.error_handler import request_should_be_json, request_does_not_match_expected_format

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


@mod_auth.route('/db', methods=['POST'])
def dbtest():
    if not request.is_json:
        return request_should_be_json()
    return make_response(jsonify({'success': 'success'}), 200)


@mod_auth.route('/test')
def test():
    return render_template('auth-test.html')


@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth-signup.html')
    # post 처리
    if not request.is_json:
        return request_should_be_json()

    data = request.get_json()
    success, data = validate_register(data)
    if not success:
        return request_does_not_match_expected_format(data)

    if app.db['users'].find_one({'email': data['email']}):
        res = {"error": "이미 존재하는 회원입니다 // this email is already registered"}
        return make_response(jsonify(res), 409)  # Conflict
    if app.db['users'].find_one({'username': data['username']}):
        res = {"error": "이미 존재하는 유저이름입니다 // this username is already used"}
        return make_response(jsonify(res), 409)  # Conflict

    data['password'] = flask_bcrypt.generate_password_hash(data['password'])
    app.db['users'].insert_one(data)
    res = jsonify({'success': '등록되었습니다 // registered successfully!'})
    return make_response(res, 200)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth-login.html')

    # post 처리
    if not request.is_json:
        return request_should_be_json()
    success, data = validate_login(request.get_json())

    if not success:
        return request_does_not_match_expected_format(data)

    user = app.db['users'].find_one({'email': data['email']})
    if not user or not flask_bcrypt.check_password_hash(user['password'], data['password']):
        res = {'error': '없거나 틀린 비밀번호입니다 // invalid password'}
        return make_response(jsonify(res), 401)

    # 올바른 아이디, 패스워드
    del data['password']
    # 정보추가
    data['username'] = str(user['username'])
    data['nickname'] = str(user['nickname'])
    # 쿠키 지정
    access_token = create_access_token(identity=data)
    refresh_token = create_refresh_token(identity=data)

    # jwt 쿠키
    res = jsonify({
        "login": True,
        'data': data,
        'access_csrf': get_csrf_token(access_token),
        'refresh_csrf': get_csrf_token(refresh_token)
    })
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)
    return make_response(res, 200)


@mod_auth.route('/logout', methods=['POST'])
def logout():
    res = jsonify({'success': '로그아웃 되었습니다'})
    unset_jwt_cookies(res)
    return make_response(res, 200)


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    res = jsonify({'refresh': True})
    set_access_cookies(res, access_token)
    return make_response(res, 200)

