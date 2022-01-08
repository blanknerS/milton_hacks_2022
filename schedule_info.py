from datetime import time
from PIL.Image import new
from bs4 import BeautifulSoup
import numpy as np
from pprint import pprint
import pandas as pd
from datetime import datetime, timedelta

path = "/Users/blakeankner/Desktop/programming/milton_hackathon_2022/schedule.html"

schedule = BeautifulSoup(open(path), "html.parser")

trs = []

for cell in schedule.find_all('tr'):
    # pprint(cell)
    tdInfo = cell.get_text('\n', strip = True)
    trs.append(tdInfo)

# pprint(trs)

times = {}

# url = r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(path) # Returns list of all tables on page
sp500_table = tables[0] # Select table of interest
df = sp500_table[0].iloc[3:]
# print(sp500_table.iloc[3])

for i in sp500_table:
    if i >= 3:
        for p in sp500_table: 
            key = sp500_table.iloc[i][0][3:8].replace("-", "").strip()
            if key == "Exte":
                key = sp500_table.iloc[i][0][12:17].replace("-", "").strip()
            times[key]= sp500_table.iloc[i][1:].values.tolist()

new_schedule = {}

for i, j in times.items():
    classes = []
    for p in j:
        try:
            class_name = p[:p.find("-")+2]
        except:
            class_name = "Free"
        classes.append(class_name)
    new_schedule[i] = classes
# pprint(new_schedule["2:20"])

orange_week = False

temp = pd.Timestamp('2022-1-6') #should be a thursday FOR TESTING 
# print(temp.dayofweek, temp.day_name())

index_of_week = (datetime.today().weekday())

index = 0

if temp.dayofweek < 5:
    if orange_week:
        index = temp.dayofweek + 5
    else:
        index = temp.dayofweek

# pprint(new_schedule["2:20"][index])

now = datetime.now().time()

def in_between(now1, start, end):
    if start <= end:
        return start <= now1 < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now1 or now1 < end

for k, v in new_schedule.items():
    class_start = datetime.strptime(k, "%H:%M")
    five_min = datetime.strptime("0:20", "%H:%M")
    check_time = datetime.strptime(str(class_start-five_min), "%H:%M:%S").time()
    if check_time <= now and now <= class_start.time():
        print(f"On {index} at {class_start}, you have: ", v[index])
