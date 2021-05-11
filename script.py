import json
import requests
from win10toast import ToastNotifier
import time
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date


def send_email(text,emailid):
    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python

    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=emailid,
        subject='slot availability notice',
        html_content="<strong>"+ text+"</strong>")
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



def notifier(prev_email):
    today = date.today()
    todays_date = today.strftime("%d-%m-%Y")
    string_to_email = ""
    toaster = ToastNotifier()
    #############################################
    district_id = [294,265,276]  # SELECT THE DISTRICT IDS THAT ARE REQUIRED BY YOU
                                 # OPEN THIS IN A BROWSER TO GET YOUR STATE ID https://cdn-api.co-vin.in/api/v2/admin/location/states
                                 # OPEN THIS IN A BROWSER USING THE STATE ID ABOVE TO GET THE DISTRICT IT
                                 # https://cdn-api.co-vin.in/api/v2/admin/location/districts/<STATE_ID>
    ############################################
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}#,'accept': 'application/json'}
    for dist in district_id:
        x = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(dist)+"&date="+todays_date,headers=header)
        data = json.loads(x.text)
        for center in data["centers"]:
            flag=0
            # if center["fee_type"] != "Paid":
            #     continue
            min_age=100
            slotsavail = []
            for session in center["sessions"]:
                if session["available_capacity"] != 0:# and session["min_age_limit"]==18:
                    flag = 1
                    slotsavail.append(session["available_capacity"])
                    if session["min_age_limit"] < min_age:
                        min_age=session["min_age_limit"]
            if flag == 1:
                print(center)
                string_to_email = string_to_email + center["name"]+"<br>"+str(center["pincode"])+"<br>"+center["block_name"]+"<br>fee type:"+center["fee_type"]+"<br>min age:"+str(min_age)+"<br>avail slots"+str(slotsavail)+"<br>-----------------<br>"
                toaster.show_toast("Vaccine available",
                                                center["name"]+"\n"+str(center["pincode"])+"\n"+center["block_name"],
                                                duration=3)
    print(string_to_email)
    if string_to_email != "":
        if string_to_email != prev_email:
            send_email(string_to_email,os.environ.get('TO_EMAIL1'))
            send_email(string_to_email,os.environ.get('TO_EMAIL2'))
        else:
            print("email skipped")
        return string_to_email
    else:
        print("empty")
        return "empty"

for x in range(10):
    prev_email="prev"
    prev_email = notifier(prev_email)
    time.sleep(500)
