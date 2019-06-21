#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: parser.py
@time: 2019/06/21
@software: PyCharm
@detail: 解析器
"""

from flask import abort, make_response, jsonify
from werkzeug.exceptions import HTTPException
from webargs import flaskparser

parser = flaskparser.FlaskParser()


@parser.error_handler
def handle_error(error, req, schema, status_code, headers):
    try:
        abort(make_response(jsonify(error.messages), status_code or parser.DEFAULT_VALIDATION_STATUS))
    except HTTPException as err:
        err.data = {
            'messages': error.messages,
            'schema': schema,
            'headers': headers
        }
        err.exc = error
        raise err
