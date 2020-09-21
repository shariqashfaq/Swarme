from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    workspaces_ids = db.relationship("Workspace", secondary="workspace_users", backref=db.backref("workers", lazy=True)) 
    date_time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship("Message", backref="user")
    channel_ids = db.relationship("Channel", secondary="channel_users", backref=db.backref("listeners", lazy=True))

class Workspace(db.Model):
    __tablename__ = "workspaces"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date_time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    channels = db.relationship("Channel", backref="workspace")

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    text = db.Column(db.String)
    date_time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean)


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    date_time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship("Message", backref="channel")
    public = db.Column(db.Boolean, nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspaces.id"), nullable=False)

workspace_users = db.Table('workspace_users',
    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column("workspace_id", db.Integer, db.ForeignKey('workspaces.id'), primary_key=True)
)

channel_users = db.Table('channel_users',
    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column("channel_id", db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)








