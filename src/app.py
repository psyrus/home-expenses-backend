
from flask import Flask
app = Flask(__name__)
from .routes import groups, groupmembers, expenses, test, users # This line needs to exist AFTER the app is initialized

@app.route("/", methods=["GET"])
def home():
    return "Home"
