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
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, render_template, request, g
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_babel import lazy_gettext as _l

from bluelog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager, csrf, migrate, babel, api
from bluelog.settings import config
from bluelog.blueprints import auth, admin, blog
from bluelog.commands import register_commands
from bluelog import apis

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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
    # 注册请求处理函数
    register_request_handlers(app)

    try:
        if app.config['BLUELOG_UPLOAD_PATH']:
            os.makedirs(app.config['BLUELOG_UPLOAD_PATH'])
    except OSError:
        pass
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
    migrate.init_app(app, db)
    babel.init_app(app)
    api.init_app(app)
    # 取消api蓝本的csrf验证
    csrf.exempt(apis.bp)

    @login_manager.user_loader
    def load_user(user_id):
        """加载登录用户"""
        user = Admin.query.get(int(user_id))
        return user

    login_manager.login_view = 'auth.login'
    login_manager.login_message = _l(login_manager.login_message)
    login_manager.login_message_category = 'warning'

    @babel.localeselector
    def get_locale():
        """获取本地语言环境"""
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def register_logging(app):
    """日志处理器"""
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logs_dir = os.path.join(basedir, 'logs')
    try:
        os.makedirs(logs_dir)
    except OSError:
        pass
    file_handler = RotatingFileHandler(os.path.join(logs_dir, 'bluelog.log'), maxBytes=10 * 1024 * 1024, backupCount=10)

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject=_l('Bluelog Application Error'),
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_blueprints(app):
    """蓝本"""
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(apis.bp, url_prefix='/api')
    # app.register_blueprint(apis.bp, subdomain='api')


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


def register_request_handlers(app):
    @app.before_request
    def before_request():
        """请求前周期函数"""
        # ----------设置本地语言环境参数---------- #
        from flask_babel import get_locale
        locale = get_locale()
        language = locale.language + '-' + locale.territory if locale.territory else locale.language
        g.locale = language

    @app.after_request
    def after_request(response):
        """请求后周期函数"""
        # ---------请求时间较长操作登记日志---------- #
        for q in get_debug_queries():
            if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n ' % (q.duration, q.context, q.statement)
                )
        return response


from bluelog.models import *
