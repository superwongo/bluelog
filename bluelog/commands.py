#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: commands.py
@time: 2019/05/23
@software: PyCharm
@detail: 自定义命令
"""

import click
import os

from bluelog.extensions import db
from bluelog.models import Admin, Category


def register_commands(app):
    """注册自定义命令"""
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(category, post, comment):
        """生成虚拟分类、文章、评论数据"""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_categories(category)

        click.echo(f'Generating {post} posts...')
        fake_posts(post)

        click.echo(f'Generating {comment} comments...')
        fake_comments(comment)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    # @click.option('--password', prompt=True, hide_input=True,
    #               confirmation_prompt=True, help='The password used to login.')
    @click.password_option(help='The password used to login.')
    def init(username, password):
        """初始化博客"""
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('The administrator already exists. updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(username=username,
                          blog_title='部落格',
                          blog_sub_title="做真实的自己",
                          name='Admin',
                          about='关于我的一些事情。')
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    @app.cli.group()
    def translate():
        """翻译命令组"""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """
        初始化新语言
        :param lang: 语言代码
        :return:
        """
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract命令失败')
        if os.system('pybabel init -i messages.pot -d bluelog/translations -l ' + lang):
            raise RuntimeError('init命令失败')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """更新子命令"""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract命令失败')
        if os.system('pybabel update -i messages.pot -d bluelog/translations'):
            raise RuntimeError('update命令失败')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """编译子命令"""
        if os.system('pybabel compile -d bluelog/translations'):
            raise RuntimeError('compile命令失败')
