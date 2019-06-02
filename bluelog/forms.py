#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: forms.py
@time: 2019/05/25
@software: PyCharm
@detail: 表单
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, URL
from flask_ckeditor import CKEditorField

from  bluelog.models import Category


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    """文章表单"""
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    """分类创建表单"""
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    """评论表单"""
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    """管理员的评论表单"""
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingsForm(FlaskForm):
    """设置表单"""
    name = StringField('Username', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()
