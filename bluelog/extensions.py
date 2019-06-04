#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: extensions.py
@time: 2019/05/21
@software: PyCharm
@detail: 扩展类实例化脚本
"""

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_babel import Babel

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
babel = Babel()

from bluelog.models import *
