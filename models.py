# _*_ coding: utf-8 _*_

from config import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    new_user = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.String(32), default='home')
    # messages = db.relationship('Message', backref='user')

    def ping(self):  # 更新用户最后访问时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return 'User {0}'.format(self.username.encode('utf-8'))


# class Message(db.Model):
#     __tablename__ = 'messages'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     type = db.Column(db.String(16))
#     raw = db.Column(db.String(256))
