from utilities.login import getData
from utilities.uidDetails import UIDinfo
from flask import Flask, request

# for (key, value) in UIDinfo.items():
#     getData({"Userid": key, "Password": value})

app = Flask(__name__)

@app.get('/leave')
def sendLeaveData():
    args = request.args
    return getData(args)