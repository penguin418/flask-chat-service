from . import mod_auth
from .. import app
from ..schemas import validate_register, validate_login

from flask import render_template, request, jsonify
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
        return jsonify({'error': 'json아님'}), 400
    
    print(request.get_json())
    return jsonify({'success': 'success'}), 200

@mod_auth.route('/test')
def test():
    return render_template('auth-test.html')

@mod_auth.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth-signup.html')
    # post 처리
    if not request.is_json:
        return jsonify({"error": "요청은 json이어야 합니다 // request should be JSON"}), 400

    print(request.get_json())
    success, data = validate_register(request.get_json())

    if success:
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        app.db['users'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!'})
        return res, 200
    else:
        return jsonify({'error': str(data)}), 400

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth-login.html')

    # post 처리
    if not request.is_json:
        return jsonify({"login": False, "error": "요청은 json이어야 합니다 // request should be JSON"}), 400
    success, data = validate_login(request.get_json())
    
    if not success:
        return jsonify({"login": False, 'error': str(data)}), 400
    
    user = app.db['users'].find_one({'email': data['email']})
    if not user or not flask_bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({"login": False, 'error': '없거나 틀린 비밀번호입니다 // invalid password'}), 401
    
    # 올바른 아이디, 패스워드
    del data['password']

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
    return res, 200

@mod_auth.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    res = jsonify({'refresh': True})
    set_access_cookies(res, access_token)
    return res, 200