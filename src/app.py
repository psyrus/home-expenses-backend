# Python standard libraries
# This line needs to exist AFTER the app is initialized
import os
import json
from oauthlib.oauth2 import WebApplicationClient
import requests
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
from flask import Flask, redirect, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from .models.models import User, AccessToken
from .routes import expenses, users, categories
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configuration
load_dotenv(".env")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
LOGGING_LEVEL = logging._nameToLevel.get(os.getenv("LOGGING_LEVEL"), 'INFO')

from .utils.authorization import secret_key, Generate_JWT, login_required
app.secret_key = secret_key

from .utils import db

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route("/test-token", methods=["GET"])
@login_required
def test_token():
    import jwt
    from flask import Response
    try:
        encoded_jwt=request.headers.get("Authorization").split("Bearer ")[1]
        decoded_jwt=jwt.decode(encoded_jwt, app.secret_key, algorithms=["HS256"], verify=True)
        logging.debug(decoded_jwt)
        return decoded_jwt
    except Exception as e:
        return Response(
            response=json.dumps({"message":"Decoding JWT Failed", "exception":e.args}),
            status=500,
            mimetype='application/json'
        )

@app.route("/reset", methods=["GET"])
def reset_db():
    from .models.base import Base
    from .utils import db
    from .utils.instantiate_database import add_test_entries
    engine = db.get_engine()
    Base.metadata.drop_all(bind=engine, checkfirst=False)
    Base.metadata.create_all(bind=engine)
    logging.info("Populating database...")
    add_test_entries()
    logging.info("Done")
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
    userinfo_response = dict(requests.get(uri, headers=headers, data=body).json())

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.get("email_verified"):
        user = users.get_user_helper_authid(oid=userinfo_response["sub"])
        if not user:
            db.add_object(
                User(
                    auth_provider_id=userinfo_response["sub"],
                    email=userinfo_response["email"],
                    username=userinfo_response["given_name"],
                )
            )
            user = users.get_user_helper_authid(oid=userinfo_response["sub"])
        
        token_content = userinfo_response.copy()
        token_expiry = datetime.now() + timedelta(days=1)
        token_content["expires"] = str(token_expiry)
        jwt_token=Generate_JWT(token_content)
        saved_token = db.add_object(AccessToken(
            registered_to_user = user.id,
            expires = token_expiry,
            token_value = jwt_token
        ))

        redirect_location = request.args.get("state")
        combined = requests.models.PreparedRequest()
        combined.prepare_url(redirect_location, {
            "token": jwt_token
        })

        return redirect(location=combined.url)
    else:
        return "User email not available or not verified by Google.", 400


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
