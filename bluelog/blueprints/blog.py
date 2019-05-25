#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: blog.py
@time: 2019/05/20
@software: PyCharm
@detail: 博客蓝本
"""

from flask import Blueprint, render_template

from bluelog.models import Post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/about')
def about():
    return render_template('blog/about.html')


@bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('/blog/post.html')
