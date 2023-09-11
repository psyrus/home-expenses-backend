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

### PostgreSQL Database

You should have a PostgreSQL database available for the backend to interact with. The database is currently hardcoded to a localhost copy running on port 5432 as can be seen in app.py or postgres.py.

Recommended method to set up the database is as follows:

1. Ensure docker desktop is installed and running
2. Run `docker-compose up --detach`

### Backend Server

1. Needs a python venv enabled

   ```bash
   python -m venv .venv
   ```

2. Once the virtual environment is installed, ensure it is activated in your terminal
3. Once in the activated virtual environment, run `pip install -r requirements.txt`
4. ~~Ensure that `serverless` is installed (<https://www.serverless.com/plugins/serverless-wsgi>)~~
5. ~~Run `serverless wsgi serve -p 5600`~~
6. Simply running the debug through the UI of VSCode (or using F5 to run the debugger) will start the server and should be able to run requests against <http://localhost:5000>
7. **Ensure that you first visit the following address to initialize the local database** (visiting it again will clear the whole database each time you do): <http://localhost:5000/reset>

### Google login flow (to create users)

1. Follow the guide to get the relevant authentication information for the OAUTH flow: <https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid>
2. Ensure that the appropriate environment variables are set in your shell for the backend server to pick them up in the app.py code (e.g.: Within your venv activate file, export/set the environment variables):
   1. GOOGLE_CLIENT_ID
   2. GOOGLE_CLIENT_SECRET
3. Once the environment variables have been set, the backend server should be restarted

## Database testing

<https://www.fusonic.net/en/blog/fusonic-test-with-databases-part-3>

## Flask Login with Google

<https://realpython.com/flask-google-login/>

[Title](https://dev.to/nagatodev/how-to-add-login-authentication-to-a-flask-and-react-application-23i7)
