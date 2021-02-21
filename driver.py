''' 
 macOS Catalina 10.15.6
 Zoom Version 5.5.2 
'''
import json
import datetime
import time
from zoomus import components, ZoomClient, util
from datetime import date
import subprocess
import pyautogui
import requests
import http.client
import pandas as pd

client = ZoomClient('dD_Z1gcSQSSe588TyzTdJQ', 'sA77ty3FNTw4gOelV18PdEWdwbJynIxjJda6')
meetingID = '6487365240'

def main():
	user_list = scrapeUsers()
	user_list.to_csv('user_list_'+date.today().strftime("%d-%m-%Y")+'.csv')
	

#Automate Zoom Deployment [Later On]
def setup(id, pswd):
	subprocess.call("usr/bin/open", "/Applications/zoom.us.app")
	time.sleep(8)
	join = pyautogui.locateCenterOnScreen('join_btn.png')
	pyautogui.moveTo(join)
	pyautogui.click()


def scrapeUsers():
	user_list = json.loads(client.user.list().content)
	df = pd.DataFrame()
	for user in user_list['users']:
		# EX: user id: Q3rbf2H1SvmNNkDqJnGvXg ---> content = json.loads(client.meeting.list(user_id='Q3rbf2H1SvmNNkDqJnGvXg').content)
		content = json.loads(client.user.get(id=user['id']).content)
		df = df.append(content, ignore_index=True)
		time.sleep(15)
	return df

def retrieveMeeting():
	conn = http.client.HTTPSConnection("api.zoom.us")
	headers = { 'authorization': "Bearer eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiI3N2JkYWY3Ny05N2YzLTRiN2MtOGJiNS04Y2NhZWY3NWEyOTUifQ.eyJ2ZXIiOjcsImF1aWQiOiJiOGE4OTJhMzMxZmQzYWNkYzM3ZDU3NTgwNTYyY2IxYSIsImNvZGUiOiJrMnkzSGVMbjcyX1EzcmJmMkgxU3ZtTk5rRHFKbkd2WGciLCJpc3MiOiJ6bTpjaWQ6azl1clJxSVJiV3Y5QlRWaXNrOHciLCJnbm8iOjAsInR5cGUiOjAsInRpZCI6MCwiYXVkIjoiaHR0cHM6Ly9vYXV0aC56b29tLnVzIiwidWlkIjoiUTNyYmYySDFTdm1OTmtEcUpuR3ZYZyIsIm5iZiI6MTYxMzg2OTYzMiwiZXhwIjoxNjEzODczMjMyLCJpYXQiOjE2MTM4Njk2MzIsImFpZCI6InJQZ2xfSXJxU0tHT2M3U2wyY1lOa1EiLCJqdGkiOiI0YjgxMGZhNS1kN2EzLTQ2NWYtOWUyOS01ZGE4NmVmZTI2NzAifQ.pTycvFFYIM-0b9GjT6TSAW5yBa2pmIx9TI1BXDZtSjWo48FsUPIdXcdJh4p4MpbFNHB-kTdA1wWINkqOWNp38w" }
	conn.request("GET", "/v2/meetings/6487365240/recordings", headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))


def json2xml(json_obj, line_padding=""):
    result_list = list()
    json_obj_type = type(json_obj)
    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))
        return "\n".join(result_list)
    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))
        return "\n".join(result_list)
    return "%s%s" % (line_padding, json_obj)

if __name__ == "__main__":
    main()