#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: admin.py
@time: 2019/05/20
@software: PyCharm
@detail: 管理员蓝图
"""

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('admin', __name__)


@bp.before_request
@login_required
def login_protect():
    """为整个蓝本添加登录保护"""
    pass


@bp.route('/settings')
def settings():
    return render_template('admin/settings.html')
