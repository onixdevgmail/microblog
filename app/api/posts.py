from flask import abort
from flask import jsonify
from flask import request
from flask_login import current_user

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Post, PostSchema


@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_all_posts_explore():
    """
    Responsible for return all posts data in system by order

    :return: all posts data
    """
    all_posts = Post.query.order_by(Post.timestamp.desc())
    result = PostSchema(many=True).dump(all_posts)
    return jsonify(result)


@bp.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    """
    Responsible for return post data

    :param id: unique post id
    :return: post data
    """
    post = Post.query.get(id)
    return PostSchema().jsonify(post)


@bp.route('/followed_posts', methods=['GET'])
@token_auth.login_required
def get_all_followed_posts():
    """
    Responsible for return user`s post data and post data of user that he follows

    :return: posts data
    """
    all_posts = current_user.followed_posts()
    result = PostSchema(many=True).dump(all_posts)
    return jsonify(result)


@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    """
    Responsible for create new post

    :return: post data
    """
    data = request.get_json() or {}
    if 'body' not in data:
        return bad_request('must include text')

    if 'language' not in data or data['language'] == 'UNKNOWN' or len(data['language']) > 5:
        data['language'] = ''
    post = Post(body=data['body'], author=current_user,
                language=data['language'])
    db.session.add(post)
    db.session.commit()
    return PostSchema().jsonify(post)


@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    current_post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    if current_post not in current_user.posts:
        abort(403)
    if 'body' in data:
        current_post.body = data['body']
    if 'language' in data:
        current_post.language = data['language']
    db.session.commit()
    return PostSchema().jsonify(current_post)


@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    current_post = Post.query.get_or_404(id)
    if current_post not in current_user.posts:
        abort(403)
    db.session.delete(current_post)
    db.session.commit()
    result = PostSchema(many=True).dump(Post.query.order_by(Post.timestamp.desc()))
    return jsonify(result)
