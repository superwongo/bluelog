#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: utils.py
@time: 2019/05/20
@software: PyCharm
@detail: 辅助函数
"""

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    """验证URL安全性"""
    # ParseResult(scheme='http', netloc='localhost:5000', path='/hello', params='', query='', fragment='')
    ref_url = urlparse(request.host_url)
    # urljoin函数用于拼接URL，若后者为不完整URL，则前后拼接；若后者为完整URL，则以后者为准
    test_url = urlparse(urljoin(request.host_url, target))
    # 防止跨域请求
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='index', **kwargs):
    """重定向回上一页面"""
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    """校验文件是否为许可类型"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']
