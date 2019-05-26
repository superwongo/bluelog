#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:Administrator
@file: emails.py
@time: 2019/05/25
@software: PyCharm
@detail: 提醒邮件函数
"""

from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from bluelog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_async_mail(subject, to, html):
    """发送异步邮件"""
    # 获取被代理的真实对象
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_async_mail(subject='New comment',
                    to=current_app.config['BLUELOG_ADMIN_EMAIL'],
                    html=f"""
                             <p>New comment in post <i>{post.title}</i>, click the link below to check:</p>
                             <p><a href="{post_url}">{post_url}</a></p>
                             <p><small style="color: #868e96">Do not reply this email.</small></p>
                         """
                    )


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_async_mail(subject='New reply',
                    to=comment.email,
                    html=f"""
                              <p>New reply for the comment you left in post 
                                  <i>{comment.post.title}</i>, click the link below to check:
                              </p>
                              <p><a href="{post_url}">{post_url}</a></p>
                              <p><small style="color: #868e96">Do not reply this email.</small></p>
                          """
                    )
