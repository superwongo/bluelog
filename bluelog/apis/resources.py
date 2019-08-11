#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: resources.py
@time: 2019/06/17
@software: PyCharm
@detail: 资源
"""

from flask import jsonify, request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, Ref, use_kwargs, doc

from bluelog.extensions import db
from .schemas import PostSchema, CategorySchema, CommentSchema
from .utils import make_pagination


@doc(
    tags=Ref('tags'),
    params=Ref('params')
)
@marshal_with(Ref('schema'))
class BaseResource(MethodResource):
    schema = None
    tags = None
    params = None


class PostListResource(BaseResource):
    schema = PostSchema
    tags = ['posts']

    def get(self):
        queryset = Post.query.order_by(Post.timestamp.desc())
        return make_pagination(queryset, 'api.posts', self.schema)

    @use_kwargs(Ref('schema'))
    def post(self, **kwargs):
        if not kwargs.get('is_valid', True):
            return jsonify(kwargs['error'].message), 422
        post = Post()
        for key, value in kwargs.items():
            setattr(post, key, value)
        db.session.add(post)
        db.session.commit()
        return post, 201


class PostResource(BaseResource):
    schema = PostSchema
    tags = ['posts']
    params = {
        'post_id': {'description': '文章ID'}
    }

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return None, 204

    @use_kwargs(Ref('schema'))
    def put(self, post_id, **kwargs):
        post = Post.query.get_or_404(post_id)
        for key, value in kwargs.items():
            setattr(post, key, value)
        db.session.commit()
        return post


class CategoryListResource(BaseResource):
    schema = CategorySchema
    tags = ['categories']

    @marshal_with(CategorySchema(many=True))
    def get(self):
        return Category.query.all()

    @use_kwargs(Ref('schema'))
    def post(self, **kwargs):
        category = Category()
        for key, value in kwargs.items():
            setattr(category, key, value)
        db.session.add(category)
        db.session.commit()
        return category, 201


class CategoryResource(BaseResource):
    schema = CategorySchema
    tags = ['categories']
    params = {
        'category_id': {'description': '分类ID'}
    }

    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return '', 204

    @use_kwargs(Ref('schema'))
    def put(self, category_id, **kwargs):
        category = Category.query.get_or_404(category_id)
        for key, value in kwargs.items():
            setattr(category, key, value)
        db.session.commit()
        return category


class CommentListResource(BaseResource):
    schema = CommentSchema
    tags = ['comments']

    def get(self):
        post_id = request.args.get('post_id')
        queryset = Comment.query.filter_by(post_id=post_id)
        return make_pagination(queryset, 'api.comments', self.schema)

    @use_kwargs(Ref('schema'))
    def post(self, **kwargs):
        comment = Comment()
        for key, value in kwargs.items():
            setattr(comment, key, value)
        db.session.add(comment)
        db.session.commit()
        return comment, 201


class CommentResource(BaseResource):
    schema = CommentSchema
    tags = ['comments']
    params = {
        'comment_id': {'description': '评论ID'}
    }

    def get(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        return comment

    def delete(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return '', 204

    @use_kwargs(Ref('schema'))
    def put(self, comment_id, **kwargs):
        comment = Comment.query.get_or_404(comment_id)
        for key, value in kwargs.items():
            setattr(comment, key, value)
        db.session.commit()
        return comment


from bluelog.models import Post, Category, Comment
