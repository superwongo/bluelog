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

from flask import Flask

from bluelog.settings import config
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.blog import blog_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app
