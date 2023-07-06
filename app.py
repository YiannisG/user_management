from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

group_permissions = db.Table('group_permissions',
                             db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
                             )


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    groups = db.Column(db.Integer, db.ForeignKey('groups.id'))
    companies = db.Column(db.Integer, db.ForeignKey('companies.id'))


class Groups(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('Users', backref='groups', lazy=True)
    permissions = db.relationship('Permissions', secondary=group_permissions, lazy='subquery',
                                  backref=db.backref('groups', lazy=True))


class Companies(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship('Users', backref='companies', lazy=True)


class Permissions(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    resource_id = db.relationship('Resources', backref='permissions', lazy=True)
    access_id = db.relationship('AccessLevels', backref='permissions', lazy=True)


class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))


class AccessLevels(db.Model):
    __tablename__ = 'access_levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))


with app.app_context():
    db.create_all()


# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Add a new company
@app.route('/company', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_company = Companies(name=data['name'])
        db.session.add(new_company)
        db.session.commit()
        return make_response(jsonify({'message': 'company created'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creating company'}), 500)
