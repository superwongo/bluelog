#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: admin.py
@time: 2019/05/20
@software: PyCharm
@detail: 管理员蓝图
"""

from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required

from bluelog.models import Post, Category, Comment
from bluelog.forms import PostForm
from bluelog.extensions import db
from bluelog.utils import redirect_back

bp = Blueprint('admin', __name__)


@bp.before_request
@login_required
def login_protect():
    """为整个蓝本添加登录保护"""
    pass


@bp.route('/settings')
def settings():
    return render_template('admin/settings.html')


@bp.route('/post/manage')
def manage_post():
    """文章管理"""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).\
        paginate(page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post update.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


@bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@bp.route('/set-comment/<int:post_id>', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment disabled.', 'info')
    else:
        post.can_comment = True
        flash('Comment enabled.', 'info')
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=post_id))


@bp.route('/comment/<int:comment_id>/approve')
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@bp.route('/comment/manage')
@login_required
def manage_comment():
    # 筛选条件：'all', 'unread', 'admin'
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    pass


@bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    pass


@bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    pass


@bp.route('/comment/new', methods=['GET', 'POST'])
def new_comment():
    pass


@bp.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    pass


@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    pass