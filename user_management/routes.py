from flask import request, make_response, jsonify

from user_management import app, db
from user_management.models import \
    User, \
    Group, \
    Company, \
    Permission


# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Add a new company
@app.route('/add_company', methods=['POST'])
def add_company():
    data = request.get_json()
    new_company = Company(name=data['name'])
    db.session.add(new_company)
    db.session.commit()
    return make_response(jsonify({'message': 'company created', 'id': new_company.id}), 201)


# Add a new permission group
@app.route('/add_group', methods=['POST'])
def add_group():
    data = request.get_json()
    if len(data['permissions']) == 0:
        raise Exception('no permission names specified')
    perms = set({})
    for perm in data['permissions']:
        perm = Permission.query.filter_by(description=perm).one()
        perms.add(perm)
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    new_group.perms = list(perms)
    db.session.commit()
    return make_response(jsonify({'message': 'permission group created', 'id': new_group.id}), 201)


# Add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    company = Company.query.filter_by(name=data['company']).one()
    group = Group.query.filter_by(name=data['group']).one()
    new_user = User(username=data['username'], company=company.id, group=group.id)
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created', 'id': new_user.id}), 201)


# edit user
@app.route('/edit_user', methods=['POST'])
def edit_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).one()
    group = Group.query.filter_by(name=data['group']).one()
    user.group = group.id
    db.session.commit()
    return make_response(jsonify({'message': 'user updated'}), 201)


# list of users
@app.route('/list_users/', methods=['GET'])
def list_users():
    page = request.args.get("page", 1)
    per_page = request.args.get("per-page", 20)
    users = User.query.paginate(page=page, per_page=per_page)
    results = {
        "results": [user.obj_to_dict() for user in users],
        "pagination": {
            "count": users.total,
            "page": page,
            "per_page": per_page,
            "pages": users.pages,
        },
    }
    return make_response(jsonify(results), 200)
