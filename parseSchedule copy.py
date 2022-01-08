from datetime import time
from PIL.Image import new
from bs4 import BeautifulSoup
import numpy as np
from pprint import pprint
import pandas as pd
from datetime import datetime

import finalTwillio


def mainFunction(user,password,phone,week,file):

	path = file
	schedule = BeautifulSoup(open(path), "html.parser")

		
	trs = []

	for cell in schedule.find_all('tr'):
	    # pprint(cell)
	    tdInfo = cell.get_text('\n', strip = True)
	    trs.append(tdInfo)

	times = {}

	tables = pd.read_html(path) # Returns list of all tables on page
	sp500_table = tables[0] # Select table of interest
	df = sp500_table[0].iloc[3:]

	for i in sp500_table: #arranging classes by row
	    if i >= 3:
	        for p in sp500_table: 
	            key = sp500_table.iloc[i][0][3:8].replace("-", "").strip()
	            if key == "Exte":
	                key = sp500_table.iloc[i][0][12:17].replace("-", "").strip()
	            times[key]= sp500_table.iloc[i][1:].values.tolist() #put classes to the time stamp

	new_schedule = {}

	for i, j in times.items():
	    classes = []
	    for p in j:
	        try:
	            class_name = p[:p.find("-")+2] #renaming classes and getting proper list
	        except:
	            class_name = "Free"
	        classes.append(class_name)
	    new_schedule[i] = classes 

	orange_week = False #Input true or false for Orange Week (True = Orange ; False = Blue)

	temp = pd.Timestamp('2022-1-6') #should be a thursday FOR TESTING 

	index_of_week = (datetime.today().weekday()) #today's date REAL APPLICATION

	index = 0 #dummy variable

	if temp.dayofweek < 5: #only work on weekdays
	    if orange_week: #shift depending on orange week or not
	        index = temp.dayofweek + 5
	    else:
	        index = temp.dayofweek

	now = datetime.strptime((datetime.now().strftime("%I:%M")), "%H:%M").time() #get current time


	# five_min = datetime.strptime("0:05", "%H:%M")

	# for i in range(3000):
	# 	now = datetime.strptime(str(now+five_min), "%H:%M:%S").time()
	# 	print(now, type(now))


	section = tables[2]["Section"].values.tolist() #classes code
	course = tables[2]["Course"].values.tolist() #classes full name

	msg = "failure"

	for k, v in new_schedule.items():
	    class_start = datetime.strptime(k, "%H:%M")
	    five_min = datetime.strptime("0:55", "%H:%M") #here we can make the time before for an alert dynamic
	    check_time = datetime.strptime(str(class_start-five_min), "%H:%M:%S").time()
	    print(f"class start: {class_start.time()}; check time: {check_time}; now: {now}")
	    if check_time <= now and now <= class_start.time(): #check if time is between the class and x minutes before
	    	print("you shuold have a class")
	    	if v[index] in section:
	        	
	        	loc = section.index(v[index])
	        	name = course[loc] #renaming
	        	msg = (f"On {index} at {class_start.time()}, you have: ", name, f"({v[index]})") #This is where you should text the info

	    else:
	    	msg = "no class atm"

	#DEFINE TWILLIO MESSAGE


	finalTwillio.send_message(msg,phone)



	





















