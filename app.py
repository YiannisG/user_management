from flask import Flask, request, make_response, jsonify
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from os import environ
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#group_permissions = db.Table('group_permissions',
#                             db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
#                             db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
#                             )


class User(db.Model):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    @validates("username")
    def validate_email(self, key, username):
        if not User.email_regex.fullmatch(username):
            raise ValueError("failed email validation")
        return username

#    groups = db.Column(db.Integer, db.ForeignKey('group.id'))
#
#
#class Group(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(80), unique=True, nullable=False)
#    users = db.relationship('Users', backref='groups', lazy=True)
#    permissions = db.relationship('Permissions', secondary=group_permissions, lazy='subquery',
#                                  backref=db.backref('groups', lazy=True))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    user = db.relationship('User', backref='user', lazy=True)

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


with app.app_context():
    # initialise database
    db.drop_all()
    db.create_all()

    # add permissions
    res_user = Resource(name='User')
    res_comp = Resource(name='Company')
    acc_vew = AccessLevel(name='View')
    acc_edit = AccessLevel(name='Edit')
    acc_add = AccessLevel(name='Add')
    acc_del = AccessLevel(name='Delete')
    db.session.add(res_user)
    db.session.add(res_comp)
    db.session.add(acc_vew)
    db.session.add(acc_edit)
    db.session.add(acc_add)
    db.session.add(acc_del)

    db.session.commit()

    perm_view_users = Permission(description="View Users", resource_id=res_user.id, access_id=acc_vew.id)
    perm_view_companies = Permission(description="View Companies", resource_id=res_comp.id, access_id=acc_vew.id)
    perm_edit_users = Permission(description="Edit Users", resource_id=res_user.id, access_id=acc_edit.id)
    perm_edit_companies = Permission(description="Edit Companies", resource_id=res_comp.id, access_id=acc_edit.id)
    perm_add_users = Permission(description="Add Users", resource_id=res_user.id, access_id=acc_add.id)
    perm_add_companies = Permission(description="Add Companies", resource_id=res_comp.id, access_id=acc_add.id)
    perm_delete_users = Permission(description="Delete Users", resource_id=res_user.id, access_id=acc_del.id)
    perm_delete_companies = Permission(description="Delete Companies", resource_id=res_comp.id, access_id=acc_del.id)
    db.session.add(perm_view_users)
    db.session.add(perm_view_companies)
    db.session.add(perm_edit_users)
    db.session.add(perm_edit_companies)
    db.session.add(perm_add_users)
    db.session.add(perm_add_companies)
    db.session.add(perm_delete_users)
    db.session.add(perm_delete_companies)

    # add company
    comp = Company(name='My Company')
    db.session.add(comp)

    db.session.commit()

    # add user
    user_admin = User(username="admin@my-company.com", company=comp.id)
    db.session.add(user_admin)

    db.session.commit()


# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Add a new company
@app.route('/company', methods=['POST'])
def create_company():
    #try:
    data = request.get_json()
    new_company = Company(name=data['name'])
    db.session.add(new_company)
    db.session.commit()
    return make_response(jsonify({'message': f'company created: {new_company.name}'}), 201)
    #except Exception:
    #    return make_response(jsonify({'message': 'error creating company'}), 500)


# Add a new company permission
#@app.route('/permission', methods=['POST'])
#def create_user():
#    try:
#        data = request.get_json()
#        new_permission = Permissions(description=data['description'])
#        db.session.add(new_permission)
#        db.session.commit()
#        return make_response(jsonify({'message': 'permission created'}), 201)
#    except Exception:
#        return make_response(jsonify({'message': 'error creating permission'}), 500)
