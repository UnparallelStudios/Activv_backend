from flask import Flask, jsonify, request
from flask_cors import CORS
from Utils.login import get_attendence_details, extract_profile_details


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
@app.route("/home", methods=["POST"])
def home() :
    if request.method == "POST" :
        response = get_user_details_n_verify_login(request.args)
        if response["Status"] == "Failure" :
            return response

        return jsonify({
                "Status": "Success",
                "Response": get_attendence_details(response["login_details"])
            })


@app.route("/profile", methods=["POST"])
def profile_pg() :
    if request.method == "POST" :
        response = get_user_details_n_verify_login(request.args)
        if response["Status"] == "Failure" :
            return response
        
        user_details = extract_profile_details(response["login_details"])
        
        return jsonify({
            "Status": "Success",
            **user_details
        })


@app.route("/login", methods=["POST"])
def login_pg() :
    if request.method == "POST" :
        response = get_user_details_n_verify_login(request.args)
        
        user_details = extract_profile_details(response["login_details"])
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


def get_user_details_n_verify_login(args) :
    user_id = args.get("Userid", default="")
    psswd = args.get("Password", default="")
    login_details = {
        "Userid": user_id,
        "Password": psswd
    }
    
    if user_id == "" :
        return {
            "Status": "Failure",
            "Response" : "User not logged in"
        }
    
    return {
        "Status": "Success",
        "Response": "User logged in",
        "login_details": login_details
    }


if __name__ == "__main__" :
    app.run(debug=True)