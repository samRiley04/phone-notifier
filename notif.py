import sys
import logging
import requests
import gspread
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig()

#find the column for today's date. If no column is found, returns 0
def findColumn():
	dateToday = datetime.datetime.today().strftime("%d/%m/%Y")
	i = 1
	while (wks.cell('1', i).value != ""):
		if (wks.cell('1', i).value == dateToday):
			return i
		i += 1
	if (wks.cell('1', i).value == ""):
		return 0

def mainFunction():
	todaysColumn = findColumn()
	if (todaysColumn == 0):
		print("No matching column found for today's date, stopping...")
		sys.exit()

	#gather data from the spreadsheet about what exams to prac today
	dataToSend = []
	i = 2
	while (wks.cell(i, todaysColumn).value != ""):
		dataToSend.append(wks.cell(i, todaysColumn).value)
		i += 1

	#create the string that we will send as notification
	notifString = "Todays exams to practice are:\n"
	for exam in dataToSend:
		notifString += "- " + exam + "\n"
	print("sending! data: ", notifString)
	#send Pushover notification
	response = requests.post(url = "https://api.pushover.net/1/messages.json", data = {
		"token": API_TOKEN,
		"user": USER_ID,
		"title": "GOOD MORNING!",
		"message": notifString
	})

def spacePress():
	while True:
		raw_input("press a key to send notif..")
		mainFunction()

#setup scheduler
sched = BlockingScheduler()

#information for posting the Pushover notifications
USER_ID = 'uwsp2gr24e877jtjrjc83w5yxvwk6w'
API_TOKEN = 'a5o3won9ek3xzsdbav7xtg3xad8wn7'

#Sheet accessing setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './auth.json'

#authorise the api
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
gc = gspread.authorize(credentials)
wks = gc.open_by_key('1Qp_4_BUmLAizLvRQe94H6kVg_Xfhr6llD9Z3G56RArM').sheet1

sched.add_job(mainFunction, 'cron', hour='0-23/1')
#sched.add_job(mainFunction, 'cron', minute='0-59/1')
sched.add_job(spacePress)
sched.start()

