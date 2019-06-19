#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: utils.py
@time: 2019/06/14
@software: PyCharm
@detail: 
"""

from flask_restful import fields


class DatetimeItem(fields.Raw):
    def format(self, value):
        return value.isoformat() + 'Z'


class RelationshipCountItem(fields.Raw):
    def format(self, value):
        return len(value)
