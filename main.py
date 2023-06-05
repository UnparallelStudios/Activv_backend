import requests as rq
from bs4 import BeautifulSoup as bs

userDetails = {"Userid": "U2108037", "Password": "210567"}
result = ""
with rq.Session() as s:
    result = s.post("https://www.rajagiritech.ac.in/stud/ktu/student/varify.asp", data=userDetails)
    result = s.get("https://www.rajagiritech.ac.in/stud/ktu/student/Leave.asp?code=2023S4AID")

soup = bs(result.content, "html.parser")
# print(soup.prettify())
dateData = soup.find_all('td', {"bgcolor": "#aaaaaa", "height": "35"})
# print(siblings)
for date in dateData:
    siblings = date.find_next_siblings("td")
    print("**************************************")
    print(date.string)
    for sibling in siblings:
        if sibling["bgcolor"] == "#9f0000":
            print(sibling.find("font").string)
        # print(sibling.find("font").string)
    print("**************************************")

# soup = bs(result.content, "html.parser")
# print(soup.prettify())