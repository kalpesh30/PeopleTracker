import requests
import json
from datetime import datetime


# Get Recent device camera analytics (in json formate)
def get_recent_analytics(serial):
    api_url = "https://api.meraki.com/api/v0/devices/" + serial + "/camera/analytics/recent"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    }

    response = requests.get(api_url,headers = headers)
    print(response.text)
    return response.json()

# Get the recent analytics zone wise of a camera with message
def get_recent_analytics_zone_wise(serial):
    response = get_recent_analytics(serial)
    npeople = []
    msg = []
    for each in response:
        stTs = str(each["startTs"])
        edTs = str(each["endTs"])
        msg.append("For zone <" + str(each["zoneId"]) + "> on " + stTs[:-14] +  " from " + stTs[12:-1] + " UTC to " + edTs[12:-1] + " UTC")
        npeople.append(each["entrances"])
        msg.append("\n Entrances: " + str(each["entrances"]) + "\n")
    return msg,npeople

# Get live camera analitics (in json formate)
def get_device_camera_live_analytics(serial):
    api_url = "https://api.meraki.com/api/v0/devices/" + serial + "/camera/analytics/live"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    }

    response = requests.get(api_url,headers = headers)
    print(response.text)
    return response.json()

# Get current camera snapshot
def get_camera_snapshot(serial,networkId):
    api_url = "https://api.meraki.com/api/v0/networks/" + networkId + "/cameras/" + serial + "/snapshot"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    }


    payload = {
    }

    response = requests.post(api_url, headers=headers, data = payload)
    i = 12
    print(response.status_code)
    while(response.status_code != 202):
        response = requests.post(api_url, headers=headers, data = payload)
        i=i-1
        if(i == 0):
            return "Unable to process the request for live image fetch. Got status code: " + str(response.status_code)
    
    response = response.json()

    return response["url"]
    
# Get the live analystics of a camera for a perticular zone with message
def get_device_camera_live_zone(zone,serial):
    response = get_device_camera_live_analytics(serial)
    msg = ""
    npeople = -1
    if zone in response["zones"]:
        npeople = response["zones"][zone]['person']
        msg = "No. of people in the zone " + zone + ": " + str(npeople) + " at time " +  str(response['ts'])
    else:
        msg = "Zone not found in the camera"
    
    return msg,npeople,response["ts"]

# Get camera analytics of all zones  with messages
def get_device_camera_live_analytics_all_zones(serial):
    response = get_device_camera_live_analytics(serial)
    npeople = []
    msg = []
    print("at time: ",response['ts'])
    for each in response["zones"].items():
        npeople.append(each)
        msg.append("No. of people in the zone " + each[0] + ": " + str(npeople[-1][1]['person']))
        print(msg[-1],'\n')
    return npeople,msg,response["ts"]

# For setting the Webex headers
def setWebexHeaders(access_token):
    header = {'Authorization' : access_token,
                'Content-Type': 'application/json; charset=utf-8'}
    return header

# For sending message to Webex Space
def send_msg(serial_mv,webex_token,webex_roomId,option,networkId):
    api_url = "https://api.ciscospark.com/v1/messages"
    access_token = "Bearer " + str(webex_token)
    
    header = setWebexHeaders(access_token)

    mesg = ""
    image = ""
    
    if(option == 1):
        image = get_camera_snapshot(serial_mv,networkId)
        msg = get_device_camera_live_analytics_all_zones(serial_mv)
        for each in msg[1]:
            mesg += each + '\n'
        

    elif(option == 2):
        image = get_camera_snapshot(serial_mv,networkId)
        zone = input("Enter the zone: ")
        msg = get_device_camera_live_zone(zone,serial_mv)
        mesg = msg[0]
        
    elif(option == 3):
        image = get_camera_snapshot(serial_mv,networkId)
        msg = get_recent_analytics_zone_wise(serial_mv)
        for each in msg[0]:
            mesg += each
    
    print(mesg)
    print(image)
    
    sp_det = {
        "roomId":webex_roomId,
        "text": mesg + '\n Camera Snapshot: ' + image
    }

    requests.post(api_url,headers=header,data=json.dumps(sp_det))

    # Y2lzY29zcGFyazovL3VzL1JPT00vN2NkMGQ2NTAtOWZmMC0xMWVhLTg5MDAtZDk0OWQwYWJkMDU5

