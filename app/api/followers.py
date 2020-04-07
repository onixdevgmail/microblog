from flask_login import current_user

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import PostSchema, User


@bp.route('/follow/<str:username>', methods=['POST'])
@token_auth.login_required
def follow(username):
    """
    Responsible for subscribing for updates on user

    :param username: users unique username
    :return: current user data
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return bad_request('User not found')
    if user == current_user:
        return bad_request('You cannot follow yourself!')
    current_user.follow(user)
    db.session.commit()
    return PostSchema().jsonify(current_user)


@bp.route('/follow/<str:username>', methods=['POST'])
@token_auth.login_required
def unfollow(username):
    """
    Responsible for unsubscribe from updates on user

    :param username: users unique username
    :return: current user data
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return bad_request('User not found')
    if user == current_user:
        return bad_request('You cannot unfollow yourself!')
    current_user.unfollow(user)
    db.session.commit()
    return PostSchema().jsonify(current_user)
