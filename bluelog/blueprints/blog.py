#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: blog.py
@time: 2019/05/20
@software: PyCharm
@detail: 博客蓝本
"""

from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, abort, make_response
from flask_login import current_user
from flask_babel import _

from bluelog.models import Post, Category, Comment
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.extensions import db
from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.utils import redirect_back

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """首页"""
    # 从查询字符串获取当前页数
    page = request.args.get('page', 1, type=int)
    # 每页数量
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    # 当前页数的记录列表
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@bp.route('/about')
def about():
    """关于"""
    return render_template('blog/about.html')


@bp.route('/category/<int:category_id>')
def show_category(category_id):
    """分类展示"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    """文章展示"""
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items

    # 如果当前用户已登录，使用管理员表单
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.date = url_for('.index')
        from_admin = True
        reviewed = True
    # 未登录，使用普通表单
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.date
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body,
                          from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        # 如果URL中reply查询参数存在，说明是回复
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # 发送邮件给被回复用户
            send_new_reply_email(replied_comment)

        db.session.add(comment)
        db.session.commit()

        # 根据登录状态显示不同的提示信息
        if current_user.is_authenticated:
            flash(_('Comment published.'), 'success')
        else:
            flash(_('Thanks, your comment will be published after reviewed.'), 'info')
            # 发送提醒邮件给管理员
            send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post.id))
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    """回复评论"""
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post', post_id=comment.post_id,
                            reply=comment_id, author=comment.author) + '#comment-form')


@bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    """切换主题"""
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response
