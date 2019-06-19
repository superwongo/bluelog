#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: __init__.py.py
@time: 2019/06/13
@software: PyCharm
@detail: Restful API
"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from bluelog.apis import urls
