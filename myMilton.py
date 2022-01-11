import requests
from bs4 import BeautifulSoup as bs
import yaml
import json
from ipregistry import IpregistryClient
from pprint import pprint
from geopy.geocoders import Nominatim
from datetime import datetime, time


def Check_Login():
        
    conf = yaml.safe_load(open('info.yml'))
    myFbUsername = conf['fb_user']['UserLogin']
    myFbPassword = conf['fb_user']['UserPassword']
    ip_key = conf['api_info']['key_ip']


    client = IpregistryClient(f"{ip_key}")  
    ipInfo = client.lookup().__dict__ #has a crap ton oof info!
    lat = ipInfo["_json"]["location"]["latitude"]
    lon = ipInfo["_json"]["location"]["longitude"]

    app = Nominatim(user_agent="tutorial")

    # demo coords
    coordinates_ma = f"{42.2567590}, {-71.0700127}"

    # get location by coordinates 
    coordinates = f"{lat}, {lon}"
    location = app.reverse(coordinates_ma, language="en").raw

    # datetime object containing current date and time
    now = datetime.now().time()

    def in_between(now, start, end):
        if start <= end:
            return start <= now < end
        else: # over midnight e.g., 23:30-04:15
            return start <= now or now < end

    if in_between(datetime.now().time(), time(8), time(10)):
        try:
            if location["address"]["amenity"] == "Milton Academy":
                with requests.Session() as s:
                    site = s.get("https://mymustangs.milton.edu/Student/index.cfm")
                    login_data = {"UserLogin":f"{myFbUsername}","UserPassword":f"{myFbPassword}"}
                    s.post("https://mymustangs.milton.edu/Student/index.cfm",login_data)
                    home_page = s.get("https://mymustangs.milton.edu/Student/index.cfm?")
                    html_file = bs(home_page.text, "html.parser")
                    print(html_file)
        except:
            print("Location not Milton")
    else:
        print("dont check location")





    # print(ipInfo)
    # milton academy: 42.256759000203935, -71.07001265996112
    # my house: 42.35425472156011, -71.07885801762838

def getSchedule():

    conf = yaml.safe_load(open('info.yml'))
    myFbUsername = conf['fb_user']['UserLogin']
    myFbPassword = conf['fb_user']['UserPassword']
    ip_key = conf['api_info']['key_ip']

    with requests.Session() as s:
        site = s.get("https://mymustangs.milton.edu/Student/index.cfm")
        login_data = {"UserLogin":f"{myFbUsername}","UserPassword":f"{myFbPassword}"}
        s.post("https://mymustangs.milton.edu/Student/index.cfm",login_data)
        home_page = s.get("https://mymustangs.milton.edu/Student/index.cfm?")
        myStuff = s.get("https://mymustangs.milton.edu/student/myschedule/fetch.cfm")
        print(bs(myStuff.text, "html.parser"))
        html_file = bs(home_page.text, "html.parser")
        with open('./google.html', 'w', encoding='utf8') as fp:
            fp.write(myStuff.text)

getSchedule()