from datetime import datetime, timedelta

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"  # The name of the table in the DB
    user_id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(60), unique=True, nullable=False)
    is_organizer = db.mapped_column(db.Boolean, default=False)

    groups = db.relationship('Group', back_populates='create_user')
    posts  = db.relationship('Post', back_populates='editor')

    def __repr__(self):
        return f"User {self.username}, is_organizer={self.is_organizer}>"

    def get_id(self):
        """A loader method for flask_login"""
        return str(self.user_id)


class Group(db.Model):
    __tablename__ = "groups"  # The name of the table in the DB
    group_id = db.mapped_column(db.Integer, primary_key=True)
    group_name = db.mapped_column(db.String(60), unique=True, nullable=False)
    description = db.mapped_column(db.String(250), nullable=False)
    create_user_id = db.mapped_column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    is_active = db.mapped_column(db.Boolean, default=True)
    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)

    create_user = db.relationship('User', back_populates='groups')
    posts = db.relationship('Post', back_populates='group')

    def __repr__(self):
        return f'"Group <group_name={self.group_name}, is_active= {self.is_active}, create_at ({self.created_at:%Y-%m-%d}>)'

    def get_id(self):
        """A loader method for flask_login"""
        return str(self.group_id)

class Post(db.Model):
    __tablename__ = "posts"  # The name of the table in the DB
    post_id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(250), nullable=False)
    context = db.mapped_column(db.String(500), nullable=False)
    date_fm = db.mapped_column(db.DateTime, default=datetime.utcnow)
    date_to = db.mapped_column(db.DateTime, nullable=False)
    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    group_id = db.mapped_column(db.Integer, db.ForeignKey("groups.group_id"), nullable=False)
    editor_id = db.mapped_column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    group = db.relationship('Group', back_populates='posts')
    editor = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f'"Post <title={self.title}" created_at={self.created_at:%Y-%m-%d}>)'


# class Editor(db.Model):
#     __tablename__ = 'editors'
#     editor_id = db.mapped_column(db.Integer, primary_key=True)
#     group_id = db.mapped_column(db.Integer, db.ForeignKey('posts.group_id'), primary_key=True)
#     user_id = db.mapped_column(db.Integer, db.ForeignKey('posts.editor_id'), primary_key=True)

#     groups = db.relationship('Post', back_populates='group')
#     posts = db.relationship('Post', back_populates='editor')
