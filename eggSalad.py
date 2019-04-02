import requests

testDict = {
	'token':'a5o3won9ek3xzsdbav7xtg3xad8wn7',
	'user':'uwsp2gr24e877jtjrjc83w5yxvwk6w',
	'message':'This is a test',
	'title':'TEST NOTIF'
}

response = requests.post(url = "https://api.pushover.net/1/messages.json", data = testDict)
print(response.text)
