# Python standard libraries
# This line needs to exist AFTER the app is initialized
import os
import json

from oauthlib.oauth2 import WebApplicationClient
import requests
from flask import Flask, redirect, request, url_for, abort
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from .models.models import User
from .routes import expenses, users, categories

from dotenv import load_dotenv

# Third-party libraries

# Configuration
load_dotenv(".env")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# wrapper
def login_required(function):
    def wrapper(*args, **kwargs):
        encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
        if encoded_jwt==None:
            return abort(401)
        else:
            return function()
    return wrapper


def Generate_JWT(payload):
    import jwt
    encoded_jwt = jwt.encode(payload, app.secret_key)
    return encoded_jwt

@login_required
@app.route("/test-token", methods=["GET"])
def test_token():
    import jwt
    from flask import Response
    encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
    try:
        decoded_jwt=jwt.decode(encoded_jwt, app.secret_key)
        print(decoded_jwt)
    except Exception as e: 
        return Response(
            response=json.dumps({"message":"Decoding JWT Failed", "exception":e.args}),
            status=500,
            mimetype='application/json'
        )

@app.route("/reset", methods=["GET"])
def reset_db():
    from sqlalchemy import (create_engine)
    from sqlalchemy_utils import database_exists, create_database, drop_database
    from .models.base import Base
    from .utils.instantiate_database import add_test_entries
    engine = create_engine(os.environ.get("DB_ADDRESS"))
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    Base.metadata.create_all(engine)
    add_test_entries()
    return "ok"


@app.route("/", methods=["GET"])
def home():
    return '<a class="button" href="/login">Google Login</a>'


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        # users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]

        user = users.get_user_helper_authid(oid=userinfo_response.json()["sub"])
        if not user:
            users.add_object_to_database(
                User(
                    auth_provider_id=userinfo_response.json()["sub"],
                    email=userinfo_response.json()["email"],
                    username=userinfo_response.json()["given_name"],
                )
            )
            user = users.get_user_helper_authid(oid=userinfo_response.json()["sub"])
        
        jwt_token=Generate_JWT(userinfo_response.json())
        print(jwt_token)
        return user.get_dict()
    else:
        return "User email not available or not verified by Google.", 400


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
