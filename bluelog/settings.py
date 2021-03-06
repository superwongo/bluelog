#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: settings.py
@time: 2019/05/20
@software: PyCharm
@detail: 配置文件
"""

import os
import sys

from flask_babel import lazy_gettext as _l
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from bluelog.apis.parser import parser

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # 加密秘钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # 调试工具拦截URL跳转
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # SQLAlchemy发生变化后是否发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # 邮件服务器地址
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    # 邮件服务器端口
    MAIL_PORT = 465
    # 邮件是否使用SSL加密
    MAIL_USE_SSL = True
    # 邮件用户名
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # 邮件密码
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # 邮件默认发送人
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # ('theme name', 'display name')
    BLUELOG_THEMES = {'perfect_blue': _l('Perfect Blue'), 'black_swan': _l('Black Swan')}
    BLUELOG_SLOW_QUERY_THRESHOLD = 1

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    # ----------国际化、本地化配置------- #
    # 支持语言列表
    LANGUAGES = ['en', 'zh_CN']
    # 默认本地语言
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    # -----------API接口解析器-------------- #
    APISPEC_WEBARGS_PARSER = parser


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.sqlite3')
    APISPEC_SPEC = APISpec(
        title='RESTFUL API',
        version='v1',
        openapi_version='3.0.2',
        plugins=[MarshmallowPlugin()],
    )
    APISPEC_SWAGGER_URL = '/swagger/'


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.sqlite3'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
