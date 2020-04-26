from functools import wraps
from flask import Response, request, g
from flask_login import current_user
from flask import redirect
from flask import url_for


def hello_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.subscribe:
            return func(*args, **kwargs)

        return redirect(url_for('main.create_subscribe'))

    return decorated_function
