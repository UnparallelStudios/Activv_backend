import requests as rq
from bs4 import BeautifulSoup as bs


def login_n_scrape(login_details, url=False) :
    """
    Function that logs in a user and scrapes data from a mentioned url
    If url is False or None, it simply logs the user in
    """
    with rq.Session() as session :
        response = session.post("https://www.rajagiritech.ac.in/stud/ktu/student/varify.asp", login_details)
        if url :
            response = session.get(url)

    return response


def extract_profile_details(login_details) :
    response = login_n_scrape(login_details, "https://www.rajagiritech.ac.in/stud/ktu/Student/Home.asp")
    
    soup = bs(response.content, "html.parser")
    for div in soup.find_all("div") :
        try :
            if div["class"] == ["scroller"] :
                # Scrape the users name
                name = div.text
                name = name[name.index(":")+1: -1].strip()
                # Scrape the users image
                imgs = soup.find_all("img")
                # Extract the photo and sign file names
                for i in imgs :
                    print(f"i[src]: {i['src']}")
                    img = i["src"]
                    if img[-14: -19: -1][-1::-1] == "Photo" :
                        img_name = img
                    elif img[-14: -18: -1][-1::-1] == "sign" :
                        sign_name = img
                
                img_url = "https://www.rajagiritech.ac.in/stud/ktu/" + img_name[3:]
                sign_url = "https://www.rajagiritech.ac.in/stud/ktu/" + sign_name[3:]
                print(img_url)

                return {
                    "User_name": name,
                    "Userid": login_details["Userid"],
                    "User_image": img_url,
                    "User_sign": sign_url
                }

        except :
            continue

    return False


def get_attendence_details(login_details):
    response = login_n_scrape(login_details, "https://www.rajagiritech.ac.in/stud/ktu/student/Leave.asp?code=2023S4AID")

    soup = bs(response.content, "html.parser")
    dateData = soup.find_all('td', {"bgcolor": "#aaaaaa", "height": "35"})

    leaveData = dict()
    user = login_details["Userid"]
    leaveData["uid"] = user
    leaveData["leaves"] = list()

    for date in dateData:
        siblings = date.find_next_siblings("td")
        dateString = date.string
        dateleaves = list()
        for i in range(0, 7):
            sibling = siblings[i]
            if sibling["bgcolor"] == "#9f0000":
                leavedate = sibling.find("font").string
                dateleaves.append(leavedate)

        leaveData["leaves"].append({dateString: dateleaves})

    return leaveData