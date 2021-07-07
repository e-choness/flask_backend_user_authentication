from datetime import datetime
from app.utils.core import db


class User(db.Model):
    """
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  
    age = db.Column(db.Integer, nullable=False)  


class UserLoginMethod(db.Model):
    """
    User Login identification table
    """
    __tablename__ = 'user_login_method'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  
    user_id = db.Column(db.Integer, nullable=False)  
    login_method = db.Column(db.String(36), nullable=False)  
    identification = db.Column(db.String(36), nullable=False) 
    access_code = db.Column(db.String(36), nullable=True)  


class Article(db.Model):
    """
    """
    __tablename__ = 'article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(20), nullable=False) 
    body = db.Column(db.String(255), nullable=False)  
    last_change_time = db.Column(db.DateTime, nullable=False, default=datetime.now)  
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  


class ChangeLogs(db.Model):
    """
    """
    __tablename__ = 'change_logs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))  
    modify_content = db.Column(db.String(255), nullable=False)  
    create_time = db.Column(db.DateTime, nullable=False)  
