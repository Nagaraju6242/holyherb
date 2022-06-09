import requests,json
from datetime import datetime
from customization.models import ShiprocketCredentials
from django.conf import settings

def send_shiprocket_req(url,data,type):
    headers = { "Authorization": "Bearer " + get_shiprocket_token(),
                "Content-Type" : "application/json",
                 }
    if(type == "post"):
        res = requests.post(url,headers=headers,data=data)
    else:
        res = requests.get(url,headers=headers,data=data)
    status_code = res.status_code
    res_text = json.loads(res.text)
    return [status_code,res_text]

def get_shiprocket_token():
    shiprocket_email = settings.SHIPROCKET_EMAIL
    shiprocket_password = settings.SHIPROCKET_PASSWORD
    creadentials = {
        "email" : shiprocket_email,
        "password" : shiprocket_password
    }
    x = ShiprocketCredentials.objects.first() if ShiprocketCredentials.objects.exists() else None
    if(x == None):
        res = requests.post("https://apiv2.shiprocket.in/v1/external/auth/login",data=creadentials)
        res = json.loads(res.text)
        ShiprocketCredentials.objects.create(token=res["token"])
        return res["token"]
    x_time = x.created_at.replace(tzinfo=None)
    diff_time = datetime.now() - x_time
    if(diff_time.days <= 8):
        return x.token
    res = requests.post("https://apiv2.shiprocket.in/v1/external/auth/login",data=creadentials)
    x.delete()
    res = json.loads(res.text)
    ShiprocketCredentials.objects.create(token=res["token"])
    return res["token"]
