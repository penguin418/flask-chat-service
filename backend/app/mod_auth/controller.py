from . import mod_auth
from .. import app
from ..schemas import validate_user

from flask import render_template, request, jsonify
import flask_bcrypt


@mod_auth.route('/db', methods=['POST'])
def dbtest():
    if not request.is_json:
        return jsonify({'error': 'json아님'}), 400

    data = request.get_json()
    print(data)

    app.db['test'].insert_one(data)

    return jsonify({'success': 'success'}), 200


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth-register.html')

    # post 처리
    if not request.is_json:
        return jsonify({"error": "요청은 json이어야 합니다 // request should be JSON"}), 400
    
    print(request.get_json())
    success, data = validate_user(request.get_json())

    if success:
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        app.db['users'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!'})
        return res, 200
    else:
        return jsonify({'error': str(data)}), 400


@mod_auth.route('/test')
def test():
    return render_template('auth-test.html')
