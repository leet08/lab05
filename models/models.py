from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

Db = SQLAlchemy()


class User(Db.Model):
    __tablename__ = 'users'
    uid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    username = Db.Column(Db.String(64), unique =True, nullable=False)
    password = Db.Column(Db.String(128), nullable=False)


class Post(Db.Model):
    __tablename__ = 'posts'
    pid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    author = Db.Column(Db.String(64), Db.ForeignKey('users.uid'), nullable=False)
    content = Db.Column(Db.String(1024), nullable=False)
    post_date = Db.Column(Db.Date, default=func.now())
    authorname = Db.relationship(User, backref='posts')

