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
        pass_out_year, branch, sem = response["Year"], response["Branch"], response["Sem"]
        if login_details["Userid"] == "" :
            return jsonify({
                "Status": "Failure",
                "Response" : "User not logged in"
            }), 401

        data = get_attendence_details(login_details, sem, branch)
        classes_count = db_manager.total_no_classes(pass_out_year, branch)
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
            }), 401

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
        pass_out_year, branch, sem = response["Year"], response["Branch"], response["Sem"]

        user_details = extract_profile_details(login_details)
        print(user_details)

        # If extraction successfully worked then that means user details entered are correct
        if not user_details :
            return jsonify({
                "Status": "Failure",
                "Response": "Wrong username or password"
            }), 401

        else :
            status = db_manager.load_db(pass_out_year, branch)
            
            data = get_attendence_details(login_details, sem, branch)
            classes_count = db_manager.total_no_classes(pass_out_year, branch)
            data["Total_classes"] = classes_count
            
            if status :
                return jsonify({
                    "Status": "Success",
                    "Response": data,
                    "User_name": user_details["User_name"],
                    "User_image": user_details["User_image"]
                })
            else :
                return jsonify({
                    "Status": "Failure",
                    "Response": "Invalid Branch or Year details"
                }), 401


@app.route("/edit/classes", methods=["POST"])
def classes_update_pg() :
    if request.method == "POST" :
        response = request.json
        classes = response["Classes"]
        pass_out_year, branch = response["Year"], response["Branch"]
        
        status = db_manager.update_classes(classes, pass_out_year, branch)
        
        if status :
            return jsonify({
                "Status": "Success",
                "Response": "Class details have been updated"
            })
        else :
            return jsonify({
                "Status": "Failure",
                "Response": "Invalid Branch or Year details"
            }), 401




if __name__ == "__main__" :
    app.run(debug=True)