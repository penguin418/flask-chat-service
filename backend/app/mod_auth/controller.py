from flask import render_template, request, jsonify
from . import mod_auth
from .. import app


@mod_auth.route('/db', methods=['POST'])
def dbtest():
    if not request.is_json:
        return jsonify({'error': 'json아님'}), 400

    data = request.get_json()
    print(data)

    app.db['test'].insert_one(data)

    return jsonify({'success': 'success'}), 200


@mod_auth.route('/test')
def test():
    return render_template('auth-test.html')
