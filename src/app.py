from flask import Flask, jsonify

app = Flask(__name__)

from .routes import groups, groupmembers, expenses

@app.route("/", methods=["GET"])
def home():
    return "Home"
