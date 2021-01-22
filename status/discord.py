import requests
import json

def fetch(url, token, post = False, get = False, delete = False, data = None):
    baseURL = "https://discordapp.com/api/" + url
    
    headers = { "Authorization":"Bot {}".format(token),
                "User-Agent":"ch0wkidarBot (https://amfoss.in, v0.1)",
                "Content-Type":"application/json", }

    if post:
        re = requests.post(baseURL, headers=headers, data=data)
    if get:
        re = requests.get(baseURL, headers=headers)
    if delete:
        re = requests.delete(baseURL, headers=headers)

    return re

class Discord(object):
    def __init__(self, obj, message = None, userID = None):
        self.obj = obj
        self.message = message
        self.userID = str(userID)

    def sendMessage(self):
        baseURL = "channels/{}/messages".format(self.obj[2])
        postedjson =  json.dumps ( {"content":self.message} )

        fetch(baseURL, token=self.obj[0], post=True, data=postedjson)

    def kickMember(self):
        baseURL = "guilds/{}/members/{}".format(self.obj[1], self.userID)
        if self.checkIfUserExists():
            re = fetch(baseURL, token=self.obj[0], delete=True)

    def checkIfUserExists(self):
        baseURL = "guilds/{}/members/{}".format(self.obj[1], self.userID)
        
        r = fetch(baseURL, token=self.obj[0], get=True)

        if int(r.status_code) == 200:
            return True

        return False
