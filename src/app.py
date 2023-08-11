from flask import Flask, jsonify
app = Flask(__name__)
from .routes import groups, groupmembers, expenses, test # This line needs to exist AFTER the app is initialized


@app.route("/", methods=["GET"])
def home():
    return "Home"
