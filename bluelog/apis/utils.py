#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: utils.py
@time: 2019/06/14
@software: PyCharm
@detail: 
"""
from flask import current_app, url_for, jsonify, request


def make_pagination(queryset, endpoint, schema):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', current_app.config['BLUELOG_POST_PER_PAGE'], type=int)
    pagination = queryset.paginate(page, per_page=per_page)
    items = pagination.items
    current_url = url_for(endpoint, page=page, _external=True)
    prev_url = url_for(endpoint, page=page - 1, _external=True) if pagination.has_prev else None
    next_url = url_for(endpoint, page=page + 1, _external=True) if pagination.has_next else None
    items = schema().dump(items, many=True).data
    return jsonify({
        'items': items,
        'current_url': current_url,
        'prev_url': prev_url,
        'next_url': next_url,
        'current_page': page,
        'per_page': per_page,
        'current_count': len(items),
        'total': pagination.total
    })
