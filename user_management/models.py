import re

from sqlalchemy.orm import validates

from user_management import db


group_permissions = db.Table('group_permissions',
                             db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
                             )


class User(db.Model):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    @validates("username")
    def validate_email(self, key, username):
        if not User.email_regex.fullmatch(username):
            raise ValueError("failed email validation")
        return username


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='users', lazy=True)
#    permissions = db.relationship('Permission', secondary=group_permissions, lazy='subquery',
#                                  backref=db.backref('groups', lazy=True))
    permissions = db.relationship('Permission', secondary=group_permissions, backref=db.backref('perms'))

    @validates('name')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship('User', backref='user', lazy=True)

    @validates('name')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    access_id = db.Column(db.Integer, db.ForeignKey('access_level.id'), nullable=False)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship('Permission', backref='permissions', lazy=True)


class AccessLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship('Permission', backref='permission', lazy=True)
