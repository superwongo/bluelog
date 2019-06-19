#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: urls.py
@time: 2019/06/14
@software: PyCharm
@detail: 
"""

from bluelog.extensions import api
from bluelog.apis.resources import PostResource, PostListResource
from bluelog.apis.resources import CategoryListResource, CategoryResource

api.add_resource(PostListResource, '/api/posts', endpoint='api.posts')
api.add_resource(PostResource, '/api/post/<int:post_id>', '/api/post/<int:id>', endpoint='api.post')

api.add_resource(CategoryListResource, '/api/categories', endpoint='api.categories')
api.add_resource(CategoryResource, '/api/category/<int:category_id>', '/api/category/<int:id>', endpoint='api.category')
