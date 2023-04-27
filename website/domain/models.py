from datetime import datetime

from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email_confirmed_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    role = db.Column(db.String(100))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    result = db.Column(db.String(150))


class Terapeut(db.Model):
    __tablename__ = 'terapeut'
    id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    function = db.Column(db.String(150))
    license = db.Column(db.String(150))
    activity_start_year = db.Column(db.Integer())

class Pacient(db.Model):
    __tablename__ = 'pacient'
    id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    terapeut_asignat = db.Column(db.Integer, db.ForeignKey('terapeut.id', ondelete="CASCADE"), nullable=False)

