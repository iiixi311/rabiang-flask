# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, \
    current_app
from flask_babel import gettext
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.blueprints.page.models import Post
from . import auth
from .forms import LoginForm, RegisterForm, UnregisterForm, ChangePasswordForm
from .models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query \
            .filter(User.email == form.email.data) \
            .first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash(gettext('You successfully logged in'), 'success')
            return redirect(request.args.get('next') or url_for('main.index'))

        flash(gettext('Invalid username or password'), 'success')

    title = gettext('Login') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Login'),
        'href': False,
    }]

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/auth/login.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()

    flash(gettext('You have been logged out'), 'success')

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()

        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.active = True

        db.session.add(user)
        db.session.commit()

        flash(gettext('You can now login.'), 'success')
        return redirect(url_for('auth.login'))

    title = gettext('Sign up') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Sign up'),
        'href': False,
    }]

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/auth/register.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/unregister', methods=['GET', 'POST'])
@login_required
def unregister():
    user = User.query.get(current_user.id)

    form = UnregisterForm()

    if form.validate_on_submit():
        Post.query \
            .filter(Post.author_id == current_user.id) \
            .update({'status': Post.STATUS_DELETED})

        db.session.delete(user)
        db.session.commit()

        flash(gettext('Your account was deleted.'), 'success')
        return redirect(url_for('page.index'))

    title = gettext('Delete Account') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Delete Account'),
        'href': False,
    }]

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/auth/unregister.html',
        form=form,
        user=user,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        if user is not None and user.verify_password(form.old_password.data):
            user.password = form.password.data

            db.session.add(user)
            db.session.commit()

            flash(gettext('You changed your password.'), 'success')
            return redirect(url_for('page.index'))

        flash(gettext('Old password is wrong.'), 'danger')
        return redirect(url_for('auth.change_password'))

    title = gettext('Change Password') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Change Password'),
        'href': False,
    }]

    return render_template(
        current_app.config.get(
            'RABIANG_SITE_THEME') + '/auth/change_password.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/reset-password')
def reset_password():
    return 'reset password'
