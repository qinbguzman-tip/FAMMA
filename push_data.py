import requests
import json

firebase_url1 = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/.json"
firebase_url2 = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/Z6N6RQOLGW/.json"

dit = {"Z6N6RQOLGW": {"zachd123": "07/07/07"}}

#requests.patch(url=firebase_url1, json=json.loads(json.dumps(dit)))
for x in ({"Selwyn": "07/09/07"}, {"Zand": "07/06/07"}, {"Cyril":"07/03/07"}): 
    requests.patch(url=firebase_url2, json=json.loads(json.dumps(x)))
    
#https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/Z6N6RQOLGW/0
#https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company