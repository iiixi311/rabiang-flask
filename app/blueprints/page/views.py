# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from flask_babel import gettext
from flask_login import login_required, current_user

from app import db
from app.blueprints.auth.models import User
from . import page
from .forms import PostForm, CommentForm
from .models import Post, Comment, Tag


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:page_num>', methods=['GET', 'POST'])
def index(page_num=1):
    posts = Post.query \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, 10, False)

    return render_template('default/page/index.html', posts=posts)


@page.route('/<slug>', methods=['GET', 'POST'])
def detail_slug(slug):
    post = Post.query \
        .filter(Post.slug == slug) \
        .first_or_404()

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment()

        comment.body = form.body.data
        comment.ip_address = request.remote_addr
        comment.post_id = post.id

        db.session.add(comment)
        db.session.commit()

        flash(gettext('Your comment has been published.'))
        return redirect(url_for('page.detail_slug', slug=post.slug))

    comments = post.comments \
        .order_by(Comment.created_timestamp.asc()) \
        .all()

    return render_template('default/page/detail.html',
                           post=post,
                           form=form,
                           comments=comments)


@page.route('/<int:post_id>')
def detail_post_id(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('default/page/detail.html', post=post)


@page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()

        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You wrote a new post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))

    return render_template('default/page/create.html', form=form)


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))

    return render_template('default/page/edit.html', form=form, post_id=post_id)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        flash(gettext('You deleted your post.'), 'success')
        return redirect(url_for('page.index'))
    else:
        return render_template('default/page/delete.html', form=form, post=post)


@page.route('/user/<username>', methods=['GET', 'POST'])
@page.route('/user/<username>/<int:page_num>', methods=['GET', 'POST'])
def user_index(username, page_num=1):
    author = User.query \
        .filter(User.username == username) \
        .first_or_404()

    posts = author.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, 10, False)

    return render_template('default/page/user.html', posts=posts)


@page.route('/tag', methods=['GET', 'POST'])
def tag_index():
    tags = Tag.query \
        .order_by(Tag.name).all()

    return render_template('default/page/tag.html', tags=tags)


@page.route('/tag/<slug>', methods=['GET', 'POST'])
@page.route('/tag/<slug>/<int:page_num>', methods=['GET', 'POST'])
def tag_post(slug, page_num=1):
    tag = Tag.query \
        .filter(Tag.slug == slug) \
        .first_or_404()

    posts = tag.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, 10, False)

    return render_template('default/page/tag_slug.html', posts=posts)
