from user_management import app, db

from user_management.models import \
    User, \
    Group, \
    Company, \
    Permission, \
    Resource, \
    AccessLevel


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
    db.session.add_all([res_user, res_comp, acc_vew, acc_edit, acc_add, acc_del])
    db.session.commit()

    perm_view_users = Permission(description="ViewUsers", resource_id=res_user.id, access_id=acc_vew.id)
    perm_view_companies = Permission(description="ViewCompanies", resource_id=res_comp.id, access_id=acc_vew.id)
    perm_edit_users = Permission(description="EditUsers", resource_id=res_user.id, access_id=acc_edit.id)
    perm_edit_companies = Permission(description="EditCompanies", resource_id=res_comp.id, access_id=acc_edit.id)
    perm_add_users = Permission(description="AddUsers", resource_id=res_user.id, access_id=acc_add.id)
    perm_add_companies = Permission(description="AddCompanies", resource_id=res_comp.id, access_id=acc_add.id)
    perm_delete_users = Permission(description="DeleteUsers", resource_id=res_user.id, access_id=acc_del.id)
    perm_delete_companies = Permission(description="DeleteCompanies", resource_id=res_comp.id, access_id=acc_del.id)
    db.session.add_all([perm_view_users, perm_view_companies, perm_edit_users, perm_edit_companies, perm_add_users,
                        perm_add_companies, perm_delete_users, perm_delete_companies])

    # add company
    comp = Company(name='MyCompany')
    db.session.add(comp)
    db.session.commit()

    # add group
    group_admin = Group(name='Admin')
    group_user = Group(name='User')
    db.session.add_all([group_admin, group_user])
    db.session.commit()

    # add user
    user_admin = User(username="admin@my-company.com", company=comp.id, group=group_admin.id)
    user_user = User(username="user@my-company.com", company=comp.id, group=group_user.id)
    db.session.add(user_admin)
    db.session.commit()

    group_admin.users = [user_admin]
    group_user.users = [user_user]
    db.session.commit()
