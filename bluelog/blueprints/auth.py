#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: auth.py
@time: 2019/05/20
@software: PyCharm
@detail: 验证蓝本
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    pass


@auth_bp.route('/logout')
def logout():
    pass
