import requests

def getInfo(call):
    r = requests.get(call)
    return r.json()