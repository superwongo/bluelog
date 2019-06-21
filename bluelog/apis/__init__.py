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

from bluelog.extensions import cors
from .resources import PostResource, PostListResource, CategoryListResource, CategoryResource, CommentListResource, \
    CommentResource

bp = Blueprint('api', __name__)
cors.init_app(bp, origins='*')

bp.add_url_rule('/posts', endpoint='posts', view_func=PostListResource.as_view('PostListResource'))
bp.add_url_rule('/post/<int:post_id>', endpoint='post', view_func=PostResource.as_view('PostResource'))

bp.add_url_rule('/categories', endpoint='categories', view_func=CategoryListResource.as_view('CategoryListResource'))
bp.add_url_rule('/category/<int:category_id>', endpoint='category', view_func=CategoryResource.as_view('CategoryResource'))

bp.add_url_rule('/comments', endpoint='comments', view_func=CommentListResource.as_view('CommentListResource'))
bp.add_url_rule('/comment/<int:comment_id>', endpoint='comment', view_func=CommentResource.as_view('CommentResource'))
