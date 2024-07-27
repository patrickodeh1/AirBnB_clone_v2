#!/usr/bin/python3
"""HBNB!"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def start_flask():
    """Starts Flask"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def display_hbnb():
    """display's HBNB!"""
    return "HBNB"


if __name__ == "__main__":
    app.run(debug=True)
