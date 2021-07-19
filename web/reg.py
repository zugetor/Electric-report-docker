from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import requests, re
from cache import timed_lru_cache

@timed_lru_cache(3600) #cache 1 hour
def getAllBuilding():
	url = "https://reg.buu.ac.th/registrar/room_timeall.asp"
	url_nosub = url[:url.rfind("/")+1]
	r = requests.get(url)
	r.encoding = r.apparent_encoding

	regex = r"<!-- Begin Page Detail -->(.*)<!-- End Page Detail -->" #Match content between 2 tag
	matches = re.search(regex, r.text, re.DOTALL)
	match = matches.group(1)

	soup = BeautifulSoup(match, 'lxml')
	row = soup.find_all("tr")[1:] #Find all row without first row
	res = []
	for i in row :
		if("room_timeall.asp" in str(i)): #Only row have room_timeall.asp is true
			a = i.find("a") #Find first a tag
			prefix = a.text
			name = i.find_all("td")[2].text
			href = url_nosub + a["href"] #Get href from a tag
			res.append({"prefix":prefix,"name":name,"url":href})
	return res

@timed_lru_cache(3600) #cache 1 hour
def getAllRoomList(url):
	url = url.replace("room_timeall.asp","room_time.asp")
	r = requests.get(url)
	r.encoding = r.apparent_encoding
	soup = BeautifulSoup(r.text, 'lxml')
	option = soup.find_all("option")
	res = []
	for i in option:
		res.append(i.text.split(" ประเภท")[0])
	return res

@timed_lru_cache(5 * 60) #cache 5 min
def getAllSchedule(url):
	url = url.replace("room_time.asp","room_timeall.asp")

	dayname = [["Monday","จันทร์"],["Tuesday","อังคาร"],["Wednesday","พุธ"],["Thursday","พฤหัสบดี"],["Friday","ศุกร์"],["Saturday","เสาร์"],["Sunday","อาทิตย์"]]
	today = datetime.now().date()
	start = today - timedelta(days=today.weekday())

	r = requests.get(url)
	r.encoding = r.apparent_encoding
	df = pd.read_html(r.text)[4][1:] #Select time table 
	df = df.rename(columns=df.iloc[0])[1:].reset_index(drop=True) #Use first row to be column and reset index
	df = df.loc[:,~df.columns.duplicated()].fillna("") #Remove duplicat col and NaN value
	if(len(df.columns) > 1):
		df.columns = df.columns.fillna('dropcol') #Fill NaN col with dropcol
		df.drop('dropcol', axis = 1, inplace = True) #Remove col dropco
		for i,day in enumerate(dayname):
			df['Day/Time'] = df['Day/Time'].replace([day[1]],start + timedelta(days=i)) #Change Day to datetime
		return df
	else: 
		return list(df.columns)

def getFloor(room_list,FRegex):
	res = []
	for room in room_list:
		matches = re.search(FRegex, room)
		if(not matches):
			res.append([-1,room])
			continue
		if(len(matches.groups()) == 0):
			return []
		f = matches.group(1)
		try:
			f = int(f)
		except:
			f = matches.group(1)
		res.append([f,room])
	res.sort()
	return res

if __name__ == '__main__':
	IF_url = "https://reg.buu.ac.th/registrar/room_timeall.asp?f_cmd=1&campusid=1&campusname=%BA%D2%A7%E1%CA%B9&bc=IF&bn=%CD%D2%A4%D2%C3%A4%B3%D0%C7%D4%B7%C2%D2%A1%D2%C3%CA%D2%C3%CA%B9%E0%B7%C8"
	LOG2_url = "https://reg.buu.ac.th/registrar/room_timeall.asp?f_cmd=1&campusid=1&campusname=%BA%D2%A7%E1%CA%B9&bc=LOG2&bn=%CD%D2%A4%D2%C3%E2%C5%A8%D4%CA%B5%D4%A1%CA%EC+2"
	IF_Room = getAllRoomList(IF_url)
	Floor_regex = "IF-([0-9]{,2})[a-zA-Z]"
	'''print(getAllBuilding())
	print("-"*50)
	print(IF_Room)
	print("-"*50)
	print(getAllSchedule(LOG2_url))
	print("-"*50)
	print(getFloor(IF_Room,Floor_regex))'''
	df = getAllSchedule(LOG2_url)
	import datetime, pytz
	tz = pytz.timezone('Asia/Bangkok')
	now1 = datetime.datetime.now(tz)
	today = datetime.date.today()
	df2 = df.loc[(df['ROOM'] == "LOG2-502") & (df['Day/Time'] == today),"{}:00-{}:00".format(now1.hour,now1.hour+1)]
	print(df2[df2.index[0]])
	if len(df2) > 0 and df2[df2.index[0]]:
		print("Reserved")
	else:
		print("Free")
	df2 = df.loc[(df['ROOM'] == "LOG2-501") & (df['Day/Time'] == today),"{}:00-{}:00".format(now1.hour,now1.hour+1)]
	print(df2[df2.index[0]])
	if len(df2) > 0 and df2[df2.index[0]]:
		print("Reserved")
	else:
		print("Free")