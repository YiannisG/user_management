# user_management

Database with flask/sqlalchemy orm db: user_management_db.png

Basic API endpoints deployed locally

### Running the API
```bash
# clone repository
docker compose up -d flask_db
docker compose build
docker compose up flask_app
```
### Commands
```bash
# add a company
## name cannot be empty
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Company1"
}' http://localhost:4000/add_company

# add a permission group
## name cannot be empty, at least 1 permission
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "NewGroup",
    "permissions": ["ViewUsers","ViewCompanies","EditCompanies"]
}' http://localhost:4000/add_group

# add a user
## username valid email format, existing company, existing permission group
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "newuser@gmail.com",
    "company": "MyCompany",
    "group": "Admin"
}' http://localhost:4000/add_user

# edit user
## only permission group
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "user@my-company.com",
    "group": "Admin"
}' http://localhost:4000/edit_user

# list users 
curl http://localhost:4000/list_users/
```

TODO:

1. Add error handling for informative error messages
2. Improve pagination on list-users. Currently only page 1 is returned
3. ADd unit testing to routes
4. Deploy to production
5. Create Views to display specific table combinations
