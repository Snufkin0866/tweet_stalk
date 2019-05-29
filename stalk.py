from requests_oauthlib import OAuth1Session
import json
from urllib import request
import config
from time import sleep
import requests

keys = {
    "CK": config.api_key,
    "CS": config.api_secret,
    "AT": config.access_token,
    "AS": config.access_secret
}

sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])
TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
userID = config.user_id
discord_webhook_url = config.discord_url

params1 = {
    "screen_name": userID,
    "count": 1,
    "include_entities": True,
    "exclude_replies": False,
    "include_rts": True
}

first = 0
while True:
    if first == 0:
        req = sess.get(TL, params=params1)
        timeline = json.loads(req.text)
        twi = timeline[0]
        first += 1
    elif first == 1:
        payload = {'content': twi['user']['name']+ 'のつぶやき' + twi['text']}
        requests.post(discord_webhook_url, data=payload)
        first += 1
    elif first == 2:
        req = sess.get(TL, params=params1)
        timeline = json.loads(req.text)
        twi = timeline[0]["text"]
        tmp = twi
        first += 1
    elif first == 3:
        req = sess.get(TL, params=params1)
        timeline = json.loads(req.text)
        twi = timeline[0]["text"]
        if(tmp != twi):
            payload = {'content': twi['user']['name'] + 'のつぶやき' + twi['text']}
            requests.post(discord_webhook_url, data=payload)
            first -= 1
    sleep(30)
    