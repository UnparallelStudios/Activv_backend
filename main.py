from login import getData
from uidDetails import UIDinfo

for (key, value) in UIDinfo.items():
    getData({"Userid": key, "Password": value})