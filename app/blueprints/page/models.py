# -*- coding: utf-8 -*-
from datetime import datetime

from flask import url_for

from app.extensions import db

post_tag = db.Table('post_tag',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now,
                                   onupdate=datetime.now)


class Post(Base):
    __tablename__ = 'post'

    STATUS_DRAFT = 0
    STATUS_PUBLIC = 1
    STATUS_DELETED = 2

    FORMAT_MARKDOWN = 0
    FORMAT_HTML = 1
    FORMAT_TEXT = 2

    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_DRAFT)
    format = db.Column(db.SmallInteger, default=FORMAT_MARKDOWN)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
                             backref=db.backref('posts', lazy='dynamic'))

    category_id = db.Column(db.Integer, db.ForeignKey('page_category.id'))
    category = db.relationship('PageCategory',
                               backref=db.backref('posts', lazy='dynamic'))

    tags = db.relationship('Tag', secondary=post_tag,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    def get_slug_url(self):
        return url_for('page.post_detail_slug', slug=self.slug)

    def get_permanent_url(self):
        return url_for('page.post_detail_id', post_id=self.id)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post: %r>' % self.title


class Comment(Base):
    __tablename__ = 'comment'

    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    body = db.Column(db.Text)
    ip_address = db.Column(db.String(64))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post',
                           backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment: %r>' % self.body


class Tag(Base):
    __tablename__ = 'tag'

    name = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag: %r>' % self.name


class PageCategory(Base):
    __tablename__ = 'page_category'

    name = db.Column(db.String(64))
    order = db.Column(db.Integer)

    parent_id = db.Column(db.Integer, db.ForeignKey('page_category.id'))
    children = db.relationship('PageCategory',
                               backref=db.backref('parent',
                                                  remote_side='PageCategory.id'),
                               lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(PageCategory, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<PageCategory: %r>' % self.name
