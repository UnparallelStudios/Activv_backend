import requests as rq
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from Scripts.login import get_attendence_details, extract_profile_details
from flask_session import Session



app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def home() :
    if request.method == "GET" :
        login_details = {
            "Userid": "U2108036",
            "Password": "210145"
        }
        return jsonify(get_attendence_details(login_details))


@app.route("/login", methods=["GET", "POST"])
def login_pg() :
    if request.method == "POST" :
        login_details = request.json
        user = extract_profile_details(login_details)
        
        # If extraction successfully worked then that means user details entered are correct
        if not user :
            return jsonify({
                "Status": "Failure"
            })
        
        else :
            # Setting up the session data
            session["User_name"] = " ".join([i.capitalize() for i in user["User_name"].split()])
            session["User_image"] = user["User_image"]
            
            print(session["User_name"], session["User_image"])
            return jsonify({
                "Status": "Success"
            })


if __name__ == "__main__" :
    app.run(debug=True)