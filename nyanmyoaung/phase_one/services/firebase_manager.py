import requests
import json
from user.settings import FCM_TOKEN, FCM_URL
noti_url = "https://fcm.googleapis.com/fcm/send" #FCM_URL
def firebase_noti(data, fcm_token): 
    headers = {"Authorization": "key=" + FCM_TOKEN}
    data = {
        "data": data,
        "registration_ids": [fcm_token]
    }
    response = requests.post(FCM_URL, headers=headers, json=data)
    response = json.loads(response.text)
    print("FCM RESPONSE", response)
    return response