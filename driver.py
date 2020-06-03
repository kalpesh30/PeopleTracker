import meraki_mv
import time

serial = "Q2GV-7HEL-HC6C"
webex_token = "MWIzNDVhZWYtN2E1Mi00MDQxLTg0NTYtNjdmY2EyMzRmNjBkMWE4ZGZhZjEtY2I1_PF84_5b4085d3-d7bd-4b73-9623-c16ea722a53a"
webex_roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vZmUxOTBjYjAtNTE2Ni0xMWVhLWIwOGUtZDllNzBlYWUyZmYx"
networkId = "L_566327653141856854"

while(True):
    print("Enter your choice: ")
    n = input("1. Get details of all zones\n2. Get details of a perticular zone\n3. Get recent analytics\n4. Exit\n\n")
    if(int(n)==4):
        exit(0)
    meraki_mv.send_msg(serial,webex_token,webex_roomId,int(n),networkId)
    time.sleep(12)