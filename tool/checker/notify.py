import requests, json
import urllib.parse

_url = "https://notify-api.line.me/api/notify" 

def linenotify(message,token):
	msg = urllib.parse.urlencode({"message":message})
	LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+token}
	session = requests.Session()
	a=session.post(_url, headers=LINE_HEADERS, data=msg)
	res = json.loads(a.text)
	if(res["message"] == "ok"):
		return True
	return False

if __name__ == '__main__':
	print(linenotify("Test","Token"))