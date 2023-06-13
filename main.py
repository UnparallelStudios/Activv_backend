from Scripts.login import getData
from Scripts.uidDetails import UIDinfo

# for (key, value) in UIDinfo.items():
#     getData({"Userid": key, "Password": value})

uid = "U2108036"
psswd = "210145"
    
def find_details(uid=uid, psswd=psswd) :
    if UIDinfo[uid] == psswd :
        return getData({"Userid": uid, "Password": psswd})

    else:
        return "Incorrect UID or Password"
    
if __name__ == "__main__" :
    print(find_details())