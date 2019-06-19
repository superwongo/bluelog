#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: resources.py
@time: 2019/06/17
@software: PyCharm
@detail: 资源
"""

from flask import current_app, url_for, jsonify
from flask_restful import Resource, marshal_with, marshal

from bluelog.extensions import db
from .serializers import serializer_post, serializer_category, ModelSerializer
from .parsers import parser_post, parser_category


class PostListResource(Resource):
    parser = parser_post()

    # @marshal_with(posts_fields, envelope='resource')
    def get(self):
        # return Post.query.all()
        args = self.parser.parse_args()
        page = args['page'] or 1
        pagination = Post.query.paginate(page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
        items = pagination.items
        current = url_for('api.posts', page=page, _external=True)
        prev = url_for('api.posts', page=page-1, _external=True) if pagination.has_prev else None
        next = url_for('api.posts', page=page+1, _external=True) if pagination.has_next else None
        return jsonify({
            'items': marshal(items, serializer_post, envelope='resource'),
            'current': current,
            'prev': prev,
            'next': next
        })

    def post(self):
        args = self.parser.parse_args()
        post = Post(
            title=args['title'],
            category=Category.query.get(args['category_id']),
            body=args['body']
        )
        db.session.add(post)
        db.session.commit()
        return post, 201


class PostResource(Resource):
    from bluelog.models import Post
    serializer_pos_test = ModelSerializer(Post, depth=1).serializer_result()

    @marshal_with(serializer_pos_test, envelope='resource')
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        args = self.parser.parse_args()
        if args['title']:
            post.name = args['title']
        if args['category_id']:
            post.category = Category.query.get(args['category_id'])
        if args['body']:
            post.body = args['body']
        db.session.commit()
        return post, 201


class CategoryListResource(Resource):
    @marshal_with(serializer_category, envelope='resource')
    def get(self):
        return Category.query.all()

    def post(self):
        return '', 201


class CategoryResource(Resource):
    parser = parser_category()

    @marshal_with(serializer_category, envelope='resource')
    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return '', 204

    def put(self, category_id):
        category = Category.query.get_or_404(category_id)
        args = self.parser.parse_args()
        if args['name']:
            category.name = args['name']
        db.session.commit()
        return category, 201


from bluelog.models import Post, Category

