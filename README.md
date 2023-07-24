# Home Expenses Backend

Designed with serverless in mind (Lambda / Azure Functions)

Python based RESTful API to interact with a backend database

## Implementation plan

Because I haven't chosen how the serverless aspect will work yet, I will just build the functions (logic) first.
I want the system to be portable to both KV datastores and RDBMS and thus will require an interface layer for each interaction with the database that should be implemented differently depending on the DB type. The interface functionality should allow better testing.

Goal is to have unit tests.

## Primary functionality

### Auth

- Sign in with Google account

### Expense Sharing Group

- Ability to create a group of people that share expenses on a monthly basis
- Administrator for the group is the person that created it
- Other users can be added to the group
  - Those members can leave the group themselves or be removed by the admin

### Expense sharing

- Member can add an expense to the group that they paid, and designate how much is owed for that expense by the other group members
  - Each other paying member can have their due amount set manually **or** the system can just be set to do an even split
  - It is possible to just select "All" which would then split the cost evenly among other group members
- At any time each member can view what they owe others
- At the end of the month, the system will created a "consolidated report" at which point it will look for transitive money owed and ensure that all transitive debts are cancelled out to reduce the total amount of money that needs to flow between members. For example if:
  - A owes B $10
  - B owes C $5
  - C owes A $5
  
  Then using the transitive owed money between the three, A need only give B $5 at the end of the month.

## Planned API Endpoints

### Group

- Add
- Update
- Get
- List
- Delete

#### Group Members

- Add
- Remove
- List

#### Expense

- Add
- Update
- Remove
- List
- Get

## Useful Resources

- <https://api.elephantsql.com/console>
- <https://www.serverless.com/blog/flask-serverless-api-in-aws-lambda-the-easy-way>
- <https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/>
- <https://www.activestate.com/blog/how-to-create-a-serverless-rest-api-with-python-and-aws-lambda/>

- <https://readme.com/pricing>
- <https://github.com/thomaxxl/safrs>
- <https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/>
- <https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application>

## Run Guide

1. Needs a python venv enabled
2. Ensure that `serverless` is installed (<https://www.serverless.com/plugins/serverless-wsgi>)
3. Run `serverless wsgi serve -p 5600`
4. Postman/Firefox can access the endpoints