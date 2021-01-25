from flask import make_response, jsonify


def request_should_be_json():
    return make_response(jsonify({"error": "요청은 json이어야 합니다 // request should be JSON"}), 400)  # Bad Request

def request_does_not_match_expected_format(data):
    res = {'error': '요청이 포맷과 일치하지 않습니다 // request_does_not_match_expected_format', 'data': str(data) }
    return make_response(jsonify(res), 400)