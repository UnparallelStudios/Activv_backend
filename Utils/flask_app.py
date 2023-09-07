from flask import Flask, jsonify, request
from flask_cors import CORS
from Utils.login import get_attendence_details, extract_profile_details
from Utils.db_manager import DbManager


app = Flask(__name__)
CORS(app)
db_manager = DbManager()

@app.route("/home", methods=["POST"])
@app.route("/", methods=["POST"])
def home() :
    if request.method == "POST" :
        response = request.json
        login_details = {key: response[key] for key in response if key in ["Userid", "Password"]}
        if login_details["Userid"] == "" :
            return jsonify({
                "Status": "Failure",
                "Response" : "User not logged in"
            })

        data = get_attendence_details(login_details)
        classes_count = db_manager.total_no_classes()
        print(data)
        data["Total_classes"] = classes_count
        
        return jsonify({
                "Status": "Success",
                "Response": data
            })


@app.route("/profile", methods=["POST"])
def profile_pg() :
    if request.method == "POST" :
        response = request.json
        login_details = {key: response[key] for key in response if key in ["Userid", "Password"]}
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
        response = request.json
        login_details = {key: response[key] for key in response if key in ["Userid", "Password"]}
        sem, branch = response["Sem"], response["Branch"]

        user_details = extract_profile_details(login_details)
        print(user_details)

        # If extraction successfully worked then that means user details entered are correct
        if not user_details :
            return jsonify({
                "Status": "Failure",
                "Response": "Wrong username or password"
            })

        else :
            status = db_manager.load_db(sem, branch)
            print(f"status: {status}")
            if status :
                return jsonify({
                    "Status": "Success",
                    "Response": "User has been successfully logged in"
                })
            else :
                return jsonify({
                    "Status": "Failure",
                    "Response": "Invalid semester or branch details"
                })


@app.route("/logout", methods=["POST"])
def logout() :
    if request.method == "POST" :
        db_manager.logout()


if __name__ == "__main__" :
    app.run(debug=True)