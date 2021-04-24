import jwt
from functools import wraps
from flask import request, abort
from app import JWT_SECRET


def validate_request(request_body):
    invalid_parameters = []

    for key in request_body.keys():
        value = request_body[key]

        if value is None:
            invalid_parameters.append(key)
        else:
            if ((type(value) is str) and not (value.strip())) or ((type(value) is int) and (value <= 0)):
                invalid_parameters.append(key)

    return tuple(invalid_parameters)


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)

        return decorated_view

    return has_role_inner


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
