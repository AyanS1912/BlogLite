from .database import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

class Follow(db.Model):
  __tablename__ ='follow'
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  uid = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
  follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
  follower = db.relationship('User',foreign_keys=[follower_id])
  following = db.relationship('User',foreign_keys=[uid])
  
class User(db.Model,UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer,autoincrement = True,primary_key = True,nullable = False)
  username = db.Column(db.String(255), unique = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  name = db.Column(db.String(255), nullable = False)
  created_date = db.Column(db.DateTime(timezone=True), default=func.now())
  profile_pic =db.Column(db.String(255))
  mimetype = db.Column(db.Text)
  post = db.relationship('Post',backref='user',passive_deletes=True)
  likes = db.relationship('Like',backref='user',passive_deletes=True)
  comments = db.relationship('Comment',backref='user',passive_deletes=True)
  following = db.relationship('Follow',secondary='follow',primaryjoin=(Follow.uid==id),secondaryjoin=(Follow.follower_id==id),cascade='all,delete', backref='user',lazy='dynamic')

  
  def is_following(self,user):
    return (self.following.filter(Follow.follower_id==user.id).count()>0) 

class Post(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  uid = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
  title = db.Column(db.String(255), nullable = False)
  desc = db.Column(db.String(255))
  post_date = db.Column(db.DateTime(timezone=True), default=func.now())
  img = db.Column(db.Text,nullable=False)
  mimetype = db.Column(db.Text, nullable=False)
  likes = db.relationship('Like',backref='post',passive_deletes=True)
  comments = db.relationship('Comment',backref='post',passive_deletes=True)
  
  
class Comment(db.Model):
  __tablename__ = 'comment'
  comm_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  pid = db. Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
  uid = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
  comment = db.Column(db.Text)
  comment_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Like(db.Model):
  __tablename__ = 'like'
  like_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  pid = db. Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
  uid = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
  liked_date = db.Column(db.DateTime(timezone=True), default=func.now())

