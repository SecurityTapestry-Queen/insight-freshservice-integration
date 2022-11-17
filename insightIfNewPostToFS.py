import requests
import json
from datetime import datetime

def whenWasTheLastTime():
    lasttime = open("lasttime.txt", "r")
    global lasttimedata
    lasttimedata = lasttime.read()
    lasttime.close()
    print("Last Check: " + lasttimedata)

def getInsightInvestigations():
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations'
    headers = {
    "X-Api-Key": "8ea43599-e617-4c6a-a106-5d9984df1332",
    "Accept-version": "investigations-preview"
    }
    params = {
    "statuses": "OPEN",
    "multi-customer": True,
    "sources": "ALERT",
    "priorities": "CRITICAL,HIGH,MEDIUM"
    }

    r = requests.get(url, headers=headers, params=params)
    global investigations
    investigations = r.json()["data"]

def checkForNew():
    for i in investigations:
        created = datetime.strptime(i["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checktime = datetime.strptime(lasttimedata, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checktime > created:
            continue
        else:
            # print(i["title"] + "\n" + i["created_time"])
            global item
            item = i
            postTicketToFS()

def updateLastTime():
    lasttime = open("lasttime.txt", "w")
    write = lasttime.write(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    lasttime.close()
    # print('Updated to current time')

def postTicketToFS():
    webhook_url = 'https://securitytapestry.freshservice.com/api/v2/tickets'

    idr_priority = 1
    if item["priority"] == 'MEDIUM':
        idr_priority = 2
    elif item["priority"] == 'HIGH':
        idr_priority = 3
    elif item["priority"] == 'CRITICAL':
        idr_priority = 4

    data = {
    "description":item["title"],
    "subject":"From InsightIDR: " + item["title"],
    "email":"insight_hook@securitytapestry.com",
    "status":2,
    "priority":idr_priority
    }
    requests.post(webhook_url, auth=('p4CWhwgKyWmyrJrKWJ', 'X'), data=json.dumps(data), headers= {'Content-Type': 'application/json'})
    # print(data)

# Execution Block
print("whenWasTheLastTime")
whenWasTheLastTime()
print("getInsightInvestigations")
getInsightInvestigations()
print("checkForNew")
checkForNew()
updateLastTime()