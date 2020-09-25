from flask import render_template, request, jsonify
from . import mod_auth
from .. import app
import flask_bcrypt


@mod_auth.route('/db', methods=['POST'])
def dbtest():
    if not request.is_json:
        return jsonify({'error': 'json아님'}), 400

    data = request.get_json()
    print(data)

    app.db['test'].insert_one(data)

    return jsonify({'success': 'success'}), 200

@mod_auth.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "요청은 json이어야 합니다 // request should be JSON"}), 400
    
    data = request.get_json()
    if data['username'] and data['email'] and data['password']:
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        app.db['users'].insert_one(data)
        res = jsonify({'success': '등록되었습니다 // registered successfully!'})
        return res, 200
    return jsonify({'error': 'wrong parameters'}), 400

@mod_auth.route('/test')
def test():
    return render_template('auth-test.html')
