#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: __init__.py.py
@time: 2019/05/20
@software: PyCharm
@detail: 初始化脚本
"""

import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from flask_login import current_user

from bluelog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager, csrf
from bluelog.settings import config
from bluelog.blueprints import auth, admin, blog
from bluelog.commands import register_commands


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    # 注册扩展（扩展初始化）
    register_extensions(app)
    # 注册日志处理器
    register_logging(app)
    # 注册蓝本
    register_blueprints(app)
    # 注册shell上下文处理函数
    register_shell_context(app)
    # 注册模板上下文处理函数
    register_template_context(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册自定义shell命令
    register_commands(app)
    return app


def register_extensions(app):
    """扩展初始化"""
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_logging(app):
    """日志处理器"""
    pass


def register_blueprints(app):
    """蓝本"""
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(auth.bp, url_prefix='/auth')


def register_shell_context(app):
    """shell上下文处理函数"""
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    """模板上下文处理函数"""
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()

        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments)


def register_errors(app):
    """错误处理函数"""
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


from bluelog.models import Admin, Category, Comment
