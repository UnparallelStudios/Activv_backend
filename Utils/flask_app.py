from flask import Flask, jsonify, request
from flask_cors import CORS
from Utils.login import get_attendence_details, extract_profile_details



app = Flask(__name__)
CORS(app)


@app.route("/home", methods=["POST"])
@app.route("/", methods=["POST"])
def home() :
    if request.method == "POST" :
        login_details = request.json
        if login_details["Userid"] == "" :
            return jsonify({
                "Status": "Failure",
                "Response" : "User not logged in"
            })

        return jsonify({
                "Status": "Success",
                "Response": get_attendence_details(login_details)
            })


@app.route("/profile", methods=["POST"])
def profile_pg() :
    if request.method == "POST" :
        login_details = request.json
        if login_details["Userid"] == "" :
            return jsonify({
                "Status": "Failure",
                "Response" : "User not logged in"
            })
        
        user_details = extract_profile_details(login_details)
        print(user_details)
        
        return jsonify({
            "Status": "Success",
            **user_details
        })


@app.route("/login", methods=["POST"])
def login_pg() :
    if request.method == "POST" :
        login_details = request.json
        user_details = extract_profile_details(login_details)
        print(user_details)

        # If extraction successfully worked then that means user details entered are correct
        if not user_details :
            return jsonify({
                "Status": "Failure",
                "Response": "Wrong username or password"
            })

        else :
            return jsonify({
                "Status": "Success",
                "Response": "User has been successfully logged in"
            })


if __name__ == "__main__" :
    app.run(debug=True)