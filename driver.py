import json
from zoomus import ZoomClient
from datetime import datetime
import subprocess
import pyautogui
import pandas as pd

client = ZoomClient('dD_Z1gcSQSSe588TyzTdJQ', 'sA77ty3FNTw4gOelV18PdEWdwbJynIxjJda6')

#Automate Zoom Deployment [Later On]
def setup(id, pswd):
	# Using Mac, and using version 5.5.2 
	subprocess.call("usr/bin/open", "/Applications/zoom.us.app")
	time.sleep(8)
	join = pyautogui.locateCenterOnScreen('join_btn.png')
	pyautogui.moveTo(join)
	pyautogui.click()


def scrapeText():
	user_list_response = client.user.list()
	user_list = json.loads(user_list_response.content)
	for user in user_list['users']:
	    user_id = user['id']
        print(json.loads(client.meeting.list(host_id=user_id).content))
