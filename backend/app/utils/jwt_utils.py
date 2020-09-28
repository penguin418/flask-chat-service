from functools import wraps
from flask import redirect
from flask_jwt_extended.view_decorators import _decode_jwt_from_request

def redirect_if_jwt_invalid(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        try:
            jwt_data = _decode_jwt_from_request(request_type='access')
        except:
            jwt_data = None
        if jwt_data and 'identity' in  jwt_data:
            return view_function(*args, **kwargs)
        else:
            return redirect('auth/login', code=302)
    return wrapper
