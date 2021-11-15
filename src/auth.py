import os
from functools import wraps

from flask import request, make_response


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usr = os.getenv('auth_usr')
        pwd = os.getenv('auth_pwd')
        auth = request.authorization

        # check authentication
        if auth and auth.username == usr and auth.password == pwd:
            return f(*args, **kwargs)

        # if authentication not successful, show login prompt
        return make_response('Could not verify user', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated
