from flask import Flask, jsonify, request, session
from flask_cors import CORS
from Utils.login import get_attendence_details, extract_profile_details
from flask_session import Session



app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def home() :
    if request.method == "GET" :
        if not session.get("User_name") :
            return jsonify({
                "Status": "Failure",
                "Response" : "User not logged in"
            })

        return jsonify({
                "Status": "Success",
                "Response": get_attendence_details(session["Login_details"])
            })


@app.route("/login", methods=["GET", "POST"])
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
            # Setting up the session data
            session["User_name"] = " ".join([i.capitalize() for i in user_details["User_name"].split()])
            session["User_image"] = user_details["User_image"]
            session["Login_details"] = login_details
            try :
                print(f"User name is: {session['User_name']}")
                print("User_name"in session)
            except Exception as ex :
                print(f"Exception is {ex}")

            return jsonify({
                "Status": "Success",
                "Response": "User has been successfully logged in"
            })

    elif request.method == "GET" :
        return {
            "Status": "Success",
            "Response": "Login Page"
        }


if __name__ == "__main__" :
    app.run(debug=True)