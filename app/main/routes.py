from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from guess_language import guess_language

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm, CommentForm, SubscribeForm
from app.models import User, Post, Comment, Country, Subscribe
from app.translate import translate
from countries_script import add_countries
from middleware import hello_middleware


@bp.before_app_request
def before_request():
    """
    Updates users last activity
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

    if not Country.query.all():
        countries = add_countries()
        for country in countries:
            new_country = Country(name=countries[country], code=country)
            db.session.add(new_country)
            db.session.commit()

    if not Subscribe.query.all():
        standard_subs = Subscribe(name='Standard', price=10)
        advanced_subs = Subscribe(name='Advanced', price=20)
        pro_subs = Subscribe(name='Pro', price=30)
        db.session.add(standard_subs)
        db.session.add(advanced_subs)
        db.session.add(pro_subs)
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
@hello_middleware
def index():
    """
    Responsible for display users posts and creating new posts

    :return: Landing page "Home"
    """
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/post/<id>', methods=['GET', 'POST'])
@login_required
@hello_middleware
def one_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id)
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        comment = Comment(body=form.post.data, commentator=current_user,
                          language=language, comment=post)
        db.session.add(comment)
        db.session.commit()
        flash(_('Your comment is now live!'))
        return redirect(url_for('main.one_post', id=id))
    return render_template('current_post.html', title=_('Post'), post=post, form=form, comments=comments)


@bp.route('/explore')
@login_required
def explore():
    """
    Responsible for display all posts in system by order

    :return: Landing page "Explore"
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    """
    Responsible for display users profile and his posts

    :param username: users unique username
    :return: Landing page "User"
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Responsible for edit users profile

    :return: Landing page "Edit Profile"
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
@hello_middleware
def follow(username):
    """
    Responsible for subscribing for updates on user

    :param username: users unique username
    :return: Redirect to "Profile"
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
@hello_middleware
def unfollow(username):
    """
    Responsible for unsubscribe from updates on user

    :param username: users unique username
    :return: Redirect to "Profile"
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    """
    Responsible for translating text

    :return: translated text
    """
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/like', methods=['POST'])
@login_required
@hello_middleware
def post_like():
    post_id = request.form['id']
    action = request.form['action']
    if post_id and action:
        try:
            post = Post.query.filter_by(id=post_id).first_or_404()
            if action == 'like':
                post.liked_by.append(current_user)
                db.session.commit()
            else:
                post.liked_by.remove(current_user)
                db.session.commit()
            return jsonify({'status': 'ok'})
        except:
            pass
    return jsonify({'status': 'ok'})


@bp.route('/subscribe', methods=['GET', 'POST'])
@login_required
def create_subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        duration = int(form.life_time.data)
        price = form.subs.data.price * duration
        if duration == 12:
            price = price - price * 0.1
        elif duration == 24:
            price = price - price * 0.2
        # print(price)

        current_user.subs_id = form.subs.data.id
        current_user.subs_expiration = datetime.today() + relativedelta(months=duration)
        db.session.commit()
        flash(_('You bought new subscribe!'))
        return redirect(url_for('main.index'))
    return render_template('subscribe.html', title=_('Buy Subscribe'), form=form)
