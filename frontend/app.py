import sys
import os

sys.path.append(os.path.abspath(".."))

from flask import Flask, render_template, request, jsonify
from main import break_cipher  # your cryptanalysis function

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.json
    ciphertext = data.get("ciphertext", "")
    result = break_cipher(ciphertext)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
