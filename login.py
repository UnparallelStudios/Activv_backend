import requests as rq
from bs4 import BeautifulSoup as bs

def getData(userDetails):
    result = ""
    with rq.Session() as s:
        result = s.post("https://www.rajagiritech.ac.in/stud/ktu/student/varify.asp", data=userDetails)
        result = s.get("https://www.rajagiritech.ac.in/stud/ktu/student/Leave.asp?code=2023S4AID")

    soup = bs(result.content, "html.parser")
    # print(soup.prettify())
    dateData = soup.find_all('td', {"bgcolor": "#aaaaaa", "height": "35"})
    # print(siblings)
    leaveData = dict()
    user = userDetails["Userid"]
    leaveData["uid"] = user
    leaveData["leaves"] = list()
    # print("**************************************")
    # print(user)
    for date in dateData:
        siblings = date.find_next_siblings("td")
        # print(date.string)
        dateString = date.string
        dateleaves = list()
        for sibling in siblings:
            if sibling["bgcolor"] == "#9f0000":
                # print(sibling.find("font").string)
                leavedate = sibling.find("font").string
                dateleaves.append(leavedate)
            # print(sibling.find("font").string)
        # print("**************************************")
        leaveData["leaves"].append({dateString: dateleaves})
    print(leaveData)
"""
{
    "uid": "2108037",
    "leaves": [
        {
            "24-May-2023": [101908/EN900E, ]
        },
         {
            "20-May-2023": [101908/EN900E, ]
        },
    ]
}

"""