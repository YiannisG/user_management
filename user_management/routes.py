from flask import request, make_response, jsonify

from user_management import app, db
from user_management.models import \
    User, \
    Group, \
    Company


# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Add a new company
@app.route('/company', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(name=data['name'])
    db.session.add(new_company)
    db.session.commit()
    return make_response(jsonify({'message': f'company created: {new_company.name}'}), 201)


# Add a new permission group
@app.route('/group', methods=['POST'])
def create_group():
    data = request.get_json()
    if len(data['permissions']) == 0:
        raise
    new_group = Group(name=data['name'], permissions=data['permissions'])
    db.session.add(new_group)
    db.session.commit()
    return make_response(jsonify({'message': f'permission group created: {new_group.name}'}), 201)


# Add a new user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(username=data['username'], company=data['company'], group=data['group'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': f'user created: {new_user.name}'}), 201)


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
