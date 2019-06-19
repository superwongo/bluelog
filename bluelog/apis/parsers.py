#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: parses.py
@time: 2019/06/17
@software: PyCharm
@detail: 请求数据解析器
"""

from flask_restful import reqparse


def parser_post():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('category_id', type=int)
    parser.add_argument('body', type=str)
    parser.add_argument('page', type=int)
    return parser


def parser_category():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    return parser
