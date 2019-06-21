#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: schemas.py
@time: 2019/06/19
@software: PyCharm
@detail: 格式化模式
"""

from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, allow_none=False)
    posts = fields.Nested('PostListSchema', many=True, dump_only=True)

    class Meta:
        strict = True


class CategoryListSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, allow_none=False)
    body = fields.Str(required=True, allow_none=False)
    timestamp = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    category_id = fields.Int(required=True, allow_none=False, load_only=True)
    category = fields.Nested('CategoryListSchema', dump_only=True)
    can_comment = fields.Boolean(dump_only=True)
    comments = fields.Nested('CommentListSchema', many=True, dump_only=True)

    class Meta:
        strict = True


class PostListSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    timestamp = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    category_id = fields.Int()
    can_comment = fields.Boolean()

    class Meta:
        strict = True


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    author = fields.Str(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)
    site = fields.Str(required=True)
    body = fields.Str(required=True, allow_none=False)
    from_admin = fields.Boolean(dump_only=True)
    reviewed = fields.Boolean(dump_only=True)
    timestamp = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    post_id = fields.Int(required=True, allow_none=False, load_only=True)
    post = fields.Nested('PostListSchema', dump_only=True)
    replied_id = fields.Int(allow_none=False, load_only=True)
    replied = fields.Nested('CommentListSchema', dump_only=True)

    class Meta:
        strict = True


class CommentListSchema(Schema):
    id = fields.Int()
    author = fields.Str()
    email = fields.Email()
    site = fields.Str()
    body = fields.Str()
    from_admin = fields.Boolean()
    reviewed = fields.Boolean()
    timestamp = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    post_id = fields.Int()
    replied_id = fields.Int()

    class Meta:
        strict = True
