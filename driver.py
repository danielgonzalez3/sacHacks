import json
from zoomus import ZoomClient
from datetime import datetime
import subprocess
import pyautogui
import pandas as pd

client = ZoomClient('dD_Z1gcSQSSe588TyzTdJQ', 'sA77ty3FNTw4gOelV18PdEWdwbJynIxjJda6')

#Automate Zoom Deployment
def setup(id, pswd):
	# Using Mac, and using version 5.5.2 
	subprocess.call("usr/bin/open", "/Applications/zoom.us.app")
	time.sleep(8)
	join = pyautogui.locateCenterOnScreen('join_btn.png')
	pyautogui.moveTo(join)
	pyautogui.click()


