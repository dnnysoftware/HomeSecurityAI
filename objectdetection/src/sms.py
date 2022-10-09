import os
from twilio.rest import Client
import datetime

def send_sms(ct):

    ct = datetime.datetime.now().replace(microsecond=0)

    account_sid = os.environ.get("ACCOUNT_SID")

    auth_token  = os.environ.get("AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ.get("TARGET_NUMBER"), 
        from_=os.environ.get("TWILIO_NUMBER"),
        body="There was somebody detected by your camera at " + str(ct))

    print(message.sid)