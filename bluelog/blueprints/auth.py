#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: auth.py
@time: 2019/05/20
@software: PyCharm
@detail: 验证蓝本
"""

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user

from bluelog.forms import LoginForm
from bluelog.models import Admin
from bluelog.utils import redirect_back

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
