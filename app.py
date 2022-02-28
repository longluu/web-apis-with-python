# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage": "/dict?=<word>"}
    return jsonify(response)


@app.get("/dict")
def dictionary():
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """

    # Get a word
    words = request.args.getlist("word")

    # Error if no input
    if not words:
        return jsonify({"status": "error", "word": words, "data": "No word provided."})

    # Iterate over all words
    response = {"words": []}
    for word in words:
        # Check exact match in dictionary
        definitions = match_exact(word)
        if definitions:
            response["words"].append({"status": "success", "word": word, "data": definitions})
        else:
            # Check approximate match
            definitions = match_like(word)
            if definitions:
                response["words"].append({"status": "partial", "word": word, "data": definitions})
            else:
                return jsonify({"status": "error", "word": word, "data": "word not found"})

    return jsonify(response)


if __name__ == "__main__":
    app.run()
