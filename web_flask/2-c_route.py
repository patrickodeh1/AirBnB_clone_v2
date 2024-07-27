#!/usr/bin/python3
"""C is fun"""
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


@app.route("/c/<text>", strict_slashes=False)
def C_is_fun(text):
    """display's C is fun"""
    new_text = text.replace("_", " ")
    return "C %s" % new_text


if __name__ == "__main__":
    app.run(debug=True)
