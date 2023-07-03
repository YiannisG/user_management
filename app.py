from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

group_permissions = db.Table('group_permissions',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    groups = db.Column(db.Integer, db.ForeignKey('groups.id'))
    companies = db.Column(db.Integer, db.ForeignKey('companies.id'))


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('Users', backref='groups', lazy=True)
    permissions = db.relationship('Permissions', secondary=group_permissions, lazy='subquery',
                                  backref=db.backref('groups', lazy=True))


class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship('Users', backref='companies', lazy=True)


class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    resource_id = db.relationship('Resources', backref='permissions', lazy=True)
    access_id = db.relationship('AccessLevels', backref='permissions', lazy=True)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))


class AccessLevels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))


db.create_all()

