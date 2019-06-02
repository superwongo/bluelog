#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: models.py
@time: 2019/05/23
@software: PyCharm
@detail: 模型
"""
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from bluelog.extensions import db


class Admin(db.Model, UserMixin):
    """管理员"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    """文章分类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # 集合关系属性
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        # 获取默认分类记录
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    """文章"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    can_comment = db.Column(db.Boolean, default=True)
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 标量关系属性
    category = db.relationship('Category', back_populates='posts')
    # 集合关系属性，设置级联删除，文章删除后，其评论会同时被删除
    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')


class Comment(db.Model):
    """评论"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # 外键
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    # 标量关系属性
    post = db.relationship('Post', back_populates='comments')
    # 指向自身的外键
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 标量关系属性
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # 集合关系属性，，设置级联删除，父评论删除后，子评论会同时被删除
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
