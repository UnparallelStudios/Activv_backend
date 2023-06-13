from flask import Flask, jsonify, request
from flask_cors import CORS
from main import find_details


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def home() :
    if request.method == "GET" :
        return jsonify(find_details(uid="U2108002", psswd="210118"))
    
if __name__ == "__main__" :
    app.run(debug=True)